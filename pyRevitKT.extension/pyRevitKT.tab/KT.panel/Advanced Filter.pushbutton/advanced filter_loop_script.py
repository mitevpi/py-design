"""Advanced Filter"""

__title__ = 'Advanced\nFilter'
__author__ = 'Petar Mitev'

from pyrevit.coreutils import Timer
timer = Timer()

from System.Collections.Generic import List
import Autodesk.Revit.DB as DB
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Transaction

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

walls = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElements()

tallwalls_ids = []

for wall in walls:
    heightp = wall.LookupParameter('Unconnected Height')
    if heightp and heightp.AsDouble() == 10.0:
        tallwalls_ids.append(wall.Id)

uidoc.Selection.SetElementIds(List[DB.ElementId](tallwalls_ids))

endtime = timer.get_time()
print(endtime)
