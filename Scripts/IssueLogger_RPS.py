__doc__ = 'This allows you to submit issues, ideas, or other types ' \
          'of feedback to a centralized log, along with the associated '   \
          'metadata of your working file.'

__title__ = 'Feedback\nTracker'
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
                           Separator, Button)

# Import others
import datetime
import csv
import os
import os.path as op

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

log_file = (r'Y:\\pyRevit Library\\Logs\\pyRevitTracking.csv')
desktop = op.expandvars('%userprofile%\\desktop')
log_file_expand = op.expandvars(log_file)

# FlexForm inputs
components = [Label('Feedback'),
               TextBox('feedback_box', Text=""),
               CheckBox('issue_toggle', 'Issue'),
               CheckBox('idea_toggle', 'Idea'),
               CheckBox('suggestion_toggle', 'Suggestion'),
               Separator(),
               Button('Send')]

form = FlexForm('User Feedback', components)
form.show()

# Metadata gather
time_stamp = datetime.datetime.now()
document_version = [revit.version, revit.host]
document_title = doc.Title
active_view = doc.ActiveView.ToString()
user_name = revit.username

# FlexForm parse
feedback_string = form.values['feedback_box']

flex_form_data = []
if form.values['suggestion_toggle'] == True:
    flex_form_data.append('Suggestion')
if form.values['idea_toggle'] == True:
    flex_form_data.append('Idea')   
if form.values['issue_toggle'] == True:
    flex_form_data.append('Issue')
elif form.values['suggestion_toggle'] == False and form.values['idea_toggle'] == False and form.values['issue_toggle'] == False:
    flex_form_data.append('N/A')

# Output formatting
version_string = '-'.join(document_version)
flex_form_string = '-'.join(flex_form_data)

all_output = [time_stamp, document_title, version_string, user_name, active_view, flex_form_string, feedback_string]

# CSV append
with open(log_file_expand, 'a') as f:
    writer = csv.writer(f)
    writer.writerow(all_output)

print time_stamp
print document_version
print document_title
print user_name
print active_view