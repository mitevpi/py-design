"""Calculates total volume of all walls in the model."""

__title__ = 'Room\nArea'
__author__ = 'Petar Mitev'


from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory

doc = __revit__.ActiveUIDocument.Document

# Creating collector instance and collecting all the walls from the model
room_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms)

# Iterate over rooms and collect Volume data

total_area = 0.0

for room in room_collector:
    area_param = room.LookupParameter('Area')
    if area_param:
        total_area = total_area + area_param.AsDouble()

# now that results are collected, print the total
print("Total Area is: {}".format(total_area))
