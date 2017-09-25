"""Advanced Collection of Data: Collects all the walls of height 10"""

__author__ = 'Petar Mitev'

import rpw
from rpw import revit, DB, UI
from System.Collections.Generic import List

param_id = DB.ElementId(DB.BuiltInParameter.WALL_USER_HEIGHT_PARAM)
parameter_filter = rpw.db.ParameterFilter(param_id, greater=1.0)
tall_walls = rpw.db.Collector(parameter_filter=parameter_filter).element_ids

uidoc.Selection.SetElementIds(List[DB.ElementId](tall_walls))
