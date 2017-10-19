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