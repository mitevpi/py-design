"""Find& Delete Unbound Rooms."""

__title__ = 'Unbound\nRooms\nPurge'
__author__ = 'Petar Mitev'


# noinspection PyUnresolvedReferences
from Autodesk.Revit.DB import FilteredElementCollector, ElementId, BuiltInCategory, Area
# noinspection PyUnresolvedReferences
from Autodesk.Revit.DB.Architecture import Room
# noinspection PyUnresolvedReferences
from Autodesk.Revit.DB.Mechanical import Space

doc = __revit__.ActiveUIDocument.Document

# Creating collector instance and collecting all the walls from the model
rms = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType()

# Iterate over rooms and collect Area data

t = Transaction(doc, "Evaluate & Delete Rooms")
t.Start()
list = []

for room in rms:
    area_param = room.LookupParameter('Area').AsDouble()
    if area_param < 0.1:
        name_param = room.LookupParameter('Name')
        id_param = room.Id
        uid_param = room.UniqueId
        list.append(id_param)
        print(name_param.AsString(),area_param,id_param.IntegerValue)

for id in list:
    doc.Delete(id)

t.Commit()
