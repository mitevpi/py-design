import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
from System.Collections.Generic import *

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

# Import RPW
from rpw import ui
from rpw.ui.forms import select_file, select_folder

# Import Other
import sys
import csv

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
uidoc=DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

# Start Transaction
t = Transaction(doc, "Collect Line Styles")
t.Start()
lineStyle = doc.Settings.Categories.get_Item(BuiltInCategory.OST_Lines)
lineStyleSubTypes = lineStyle.SubCategories
existingLines = []
existingLineIds = []
for i in lineStyleSubTypes:
    name = i.Name
    ID = i.Id
    existingLines.append(name)
    existingLineIds.append(ID)

# End Transaction
t.Commit()
t.Dispose()

# Open & Parse Standards File
standardsList = []
filepath = select_file('LineStyle Standards (*.csv)|*.csv', 'Select LineStyle Standards')
with open(filepath) as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		standardsList.append(row)

print standardsList
# Check 

# Show Results
print existingLines
