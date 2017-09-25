"""Collects sheets with a specified parameter"""

__title__ = 'Sheet\nCollector'
__author__ = 'Petar Mitev'


from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Transaction

doc = __revit__.ActiveUIDocument.Document

# Creating collector instance and collecting the sheets
sheets_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets).WhereElementIsNotElementType().ToElements()

t = Transaction(doc, "Update Sheet Parameters")
t.Start()

for sheet in sheets_collector:
    custom_param = sheet.LookupParameter('CUSTOM_PARAM')
    if custom_param:
        custom_param.Set("Example.value")

t.Commit()
