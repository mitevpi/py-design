"""Delete all model elements of category"""

__title__ = 'Wipe Elements\nof Category'
__author__ = 'Petar Mitev'

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

#rpw
import rpw
from rpw import revit, db, ui, DB, UI
from rpw.db.element import Element
from rpw.utils.dotnet import clr, Process
from rpw.utils.logger import logger
from rpw.base import BaseObject, BaseObjectWrapper

#document
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

#ui
search_param = rpw.ui.forms.TextInput('Wipe Category', default='Walls', description='Enter a Category to Wipe', sort=True, exit_on_close=True)

#collect elements
element_collector = db.Collector(of_category=search_param, is_type=False)
elements = element_collector.elements

print(element_collector)
print(elements)

with db.Transaction('Wipe Elements of Category'):
	[revit.doc.Delete(id) for id in element_collector.element_ids]