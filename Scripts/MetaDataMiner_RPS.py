__doc__ = 'Mines the document for relevant metadata, and converts it ' \
          'into a seriealized JSON schema.'

__title__ = 'Metadata\nMiner'
__author__ = 'Petar Mitev'

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

import clr
# Import RevitAPI
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

# Import RPW
import rpw
from rpw import revit, db, ui, DB, UI
from rpw.db.element import Element
from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, CheckBox,
                           Separator, Button, select_file, select_folder)

# Import others
import datetime
import csv
import itertools
import os
import os.path as op
import json

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

log_file = (r'Y:\\pyRevit Library\\Logs\\pyRevitTracking.csv')
desktop = op.expandvars('%userprofile%\\desktop')
data_file = os.path.join(desktop, "metadata.txt")

# FlexForm inputs
components = [Label('Type of Mining'),
               CheckBox('mine_document', 'Basic'),
               CheckBox('mine_standard', 'Standards'),
               CheckBox('mine_model', 'Model'),
               Separator(),
               Button('Run')]

form = FlexForm('Metadata Mining', components)
form.show()

# Metadata gather - Document
time_stamp = datetime.datetime.now()
document_version = revit.version
document_host = revit.host
document_title = doc.Title
active_view = doc.ActiveView.ToString()
user_name = revit.username

# Metadata dictionary - Document
if form.values['mine_document'] == True:
    docDict = {}
    docDict['Time Stamp'] = str(time_stamp)
    docDict['Document Title'] = str(document_title)
    docDict['Document Version'] = str(document_version)
    docDict['Document Host'] = str(document_host)
    docDict['Username'] = str(user_name)
    docDict['Active View'] = str(active_view)

# Metadata gather - Line Standards
if form.values['mine_standard'] == True:
    # Read standards CSV
    lineStandardsList = []
    filepath = select_file('LineStyle Standards (*.csv)|*.csv', 'Select LineStyle Standards')
    with open(filepath) as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		lineStandardsList.append(row)
    lineStandardsList = list(itertools.chain(*lineStandardsList))

    # Collect Line Styles from Active Document
    lineStyle = doc.Settings.Categories.get_Item(BuiltInCategory.OST_Lines)
    lineStyleSubTypes = lineStyle.SubCategories
    existLineDict = {}
    existingLines = []
    existingLineIds = []
    for i in lineStyleSubTypes:
        existLine = {}
        name = i.Name
        ID = i.Id
        existingLines.append(name)
        existingLineIds.append(ID)
        existLine['Name'] = str(i.Name)
        existLine['Id'] = str(i.Id)
        existLineDict[i.Name] = existLine

    # Check Standards Against Existing Line Styles
    nonconformList = []
    nonconformIdList = []
    conformList = []
    conformIdList = []
    conformDict = {}
    nonconformDict = {}
    for i in lineStyleSubTypes:
        if i.Name not in lineStandardsList:
            nonConform = {}
            nonconformList.append(i.Name)
            nonconformIdList.append(i.Id)
            nonConform['Name'] = str(i.Name)
            nonConform['Id'] = str(i.Id)
            nonconformDict[i.Name] = nonConform
        else:
            conform = {}
            conformList.append(i.Name)
            conformIdList.append(i.Id)
            conform['Name'] = str(i.Name)
            conform['Id'] = str(i.Id)
            conformDict[i.Name] = conform

# Metadata dictionary - Workset Standards
if form.values['mine_standard'] == True:
    docWorksetsDict = {}
    collector = FilteredWorksetCollector(doc)
    for i in collector:
        worksetProperties = {}
        worksetProperties['Name'] = str(i.Name)
        worksetProperties['Kind'] = str(i.Kind)
        worksetProperties['Owner'] = str(i.Owner)
        worksetProperties['Id'] = str(i.Id)
        docWorksetsDict[i.Name] = worksetProperties

# Metadata dictionary - STANDARDS
if form.values['mine_standard'] == True:
    standardDict = {}

    # Line Standards
    standardDict['Existing Linestyle Count'] = len(existingLines)   
    standardDict['Nonconforming Linestyle Count'] = len(nonconformList)
    standardDict['Conforming Linestyle Count'] = len(conformList)

    # NEW Line Standards
    standardDict['Existing Linestyle Data'] = existLineDict
    standardDict['Conforming Linestyle Data'] = conformDict
    standardDict['Non-Conforming Linestyle Data'] = nonconformDict

    # Workset Standards
    standardDict['Worksets'] = docWorksetsDict

# Metadata dictionary - PARENT
parentDict = {}
if form.values['mine_document'] == True:
    parentDict['Document'] = docDict
if form.values['mine_standard'] == True:
    parentDict['Standards'] = standardDict

# JSON formatting
print json.dumps(parentDict, sort_keys=True, ensure_ascii=False, indent=4)

# Export to desktop
with open(data_file, 'w') as outfile:
    json.dump(parentDict, outfile)