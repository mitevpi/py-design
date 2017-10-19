"""Delete all model elements of category"""

__title__ = 'Wipe Elements\nof Category'
__author__ = 'Petar Mitev'

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)
import clr

#rpw
import rpw
from rpw import revit, db, ui

#Import module for Revit
clr.AddReference("RevitNodes")
clr.AddReference('ProtoGeometry')
clr.ImportExtensions(Revit.Elements)

#import module for the Document and transactions
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

#import Revit API
clr.AddReference('RevitAPI')

#document
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

#ui
search_param = rpw.ui.forms.TextInput('Wipe Category', default='Wall', description='Enter a Category to Wipe', sort=True, exit_on_close=True)

#collect elements
element_collector = db.Collector(of_class=search_param)

element_list = []

for i in element_collector:
    id_param = i.Id
    uid_param = i.UniqueId
    element_list.append(id_param)

print(element_list)

#transaction start
#t = Transaction(doc, "Wipe Elements")
#t.Start()

#view = doc.ActiveView

#t.Commit()
#t.Dispose()