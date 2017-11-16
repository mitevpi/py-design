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

# Import others
import datetime

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

time_stamp = datetime.datetime.now()
document_version = [revit.version, revit.host]
document_title = doc.Title
active_view = doc.ActiveView.ToString()
user_name = revit.username

print time_stamp
print document_version
print document_title
print user_name
print active_view