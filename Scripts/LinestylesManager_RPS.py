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
from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, TextBox, Separator, Button)

# Import Other
import sys
import csv
import itertools

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
uidoc=DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

# Open & Parse Standards File
standardsList = []
filepath = select_file('LineStyle Standards (*.csv)|*.csv', 'Select LineStyle Standards')
with open(filepath) as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		standardsList.append(row)
standardsList = list(itertools.chain(*standardsList))

# Collect Line Styles from Active Document
lineStyle = doc.Settings.Categories.get_Item(BuiltInCategory.OST_Lines)
lineStyleSubTypes = lineStyle.SubCategories
existingLines = []
existingLineIds = []
for i in lineStyleSubTypes:
    name = i.Name
    ID = i.Id
    existingLines.append(name)
    existingLineIds.append(ID)

# Check Standards Against Existing Line Styles
nonconformList = []
nonconformIdList = []
conformList = []
conformIdList = []
comboBoxBuild = []
for i in lineStyleSubTypes:
    if i.Name not in standardsList:
        nonconformList.append(i.Name)
        nonconformIdList.append(i.Id)
    else:
        conformList.append(i.Name)
        conformIdList.append(i.Id)
        comboBoxBuild.append("'{}': '{}'".format(i.Name, i.Name))

comboBoxString = ','.join(comboBoxBuild)

# Collect Noncomforming Line Elements in Revit
lineCollector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Lines).WhereElementIsNotElementType().ToElements()
lineElementList = []
nonconformLineElements = []
nonconformLineElementNames = []
nonconformLineElementNamesUQ = []
flexFormBuild = []
tempDict = {}
templateDict = {}
inputCount = 0
for i in lineCollector:
    if i.LineStyle.Name in nonconformList:
        # collect all nonconforming line elements from Revit
        nonconformLineElements.append(i)
        nonconformLineElementNames.append(i.LineStyle.Name)
        if i.LineStyle.Name not in nonconformLineElementNamesUQ:
            # add to unique names list
            nonconformLineElementNamesUQ.append(i.LineStyle.Name)
            # add unique names to flexform UI
            flexFormBuild.append(eval("Label({})".format("'{}'".format(i.LineStyle.Name))))
            lineString = ''.join(e for e in i.LineStyle.Name if e.isalnum())
            flexFormBuild.append(eval("ComboBox({}, {})".format("'" + lineString + "'","{" + comboBoxString + "}")))
            inputCount = inputCount + 1

            # master dictionary append for debug
            tempDict[lineString] = i.LineStyle.Name

    else:
        templateDict[i.LineStyle.Name] = i.LineStyle

# Flex Form
flexFormBuild.append(eval("Button('Run')"))
components = flexFormBuild
form = FlexForm('Line Style Manager', components)
form.show()
userInput = form.values

# Show Results
print "Number of Line Styles in Current File: {}".format( len( existingLines ))
print existingLines
print "Number of Line Styles in Standards: {}".format( len( standardsList ))
print standardsList
print "Number of Nonconforming Line Styles: {}".format( len( nonconformList ))
print nonconformList
print "Number of Nonconforming Line Elements: {}".format( len( nonconformLineElements ))
print nonconformLineElementNamesUQ

# Create Master Dictionary for Line Style Overrides
masterDict = {}
for i in userInput:
    newKey = tempDict[i]
    newValue = userInput[i]
    masterDict[newKey] = newValue

t = Transaction(doc, "Color Override Rooms")
t.Start()

# Change Line Styles in Revit Document
for i in nonconformLineElements:
    #print the names of the line styles to convert to
    newName = masterDict[i.LineStyle.Name]
    print newName
    print templateDict[newName]
    print i.LineStyle
    print '____________'

t.Commit()
t.Dispose()