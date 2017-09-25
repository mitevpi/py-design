import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)
import clr

#random
import random
from random import randint

#Import module for Revit
clr.AddReference("RevitNodes")
clr.AddReference('ProtoGeometry')
import Revit
clr.ImportExtensions(Revit.Elements)

#import module for the Document and transactions
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

#import Revit API
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.DB.Analysis import *

#document
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

#import module for colors
def randColor():
    rand_color = Color(random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256))
    return rand_color

#collect rooms
room_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType()

rooms =[]
unique_departments = []

#check the rooms for department parameter
for room in room_collector:
    department_param = room.LookupParameter('Department Class')

    #if there is a department parameter, add it to a list
    if department_param.AsString != None:
        rooms.append(room)

    if department_param.AsString() not in unique_departments:
        unique_departments.append(department_param.AsString())

#colors
graphics_overrides = {}
colors = []

#get hatch pattern from Revit API
ftarget = FillPatternTarget.Drafting
solid_fill = FillPatternElement.GetFillPatternElementByName(doc, ftarget, "Solid fill")

#generate colors based on departments
for d in unique_departments:
    color = randColor()
    graphics_overrides[d] = OverrideGraphicSettings()
    graphics_overrides[d].SetProjectionFillColor(color)
    graphics_overrides[d].SetProjectionFillPatternId(solid_fill.Id)

#transaction start
t = Transaction(doc, "Color Override Rooms")
t.Start()

view = doc.ActiveView

#assign colors
for room in rooms:
    d = room.LookupParameter('Department Class').AsString()
    view.SetElementOverrides(room.Id, graphics_overrides[d])

t.Commit()
t.Dispose()