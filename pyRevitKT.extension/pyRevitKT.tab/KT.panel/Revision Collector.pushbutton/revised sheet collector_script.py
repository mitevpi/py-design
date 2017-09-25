<<<<<<< HEAD
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
=======
"""Collect and list all revised sheets"""

__title__ = 'Revision\nCollector'

from revitutils import doc
from scriptutils import this_script
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory

this_script.output.print_md('**LIST OF REVISIONS:**')
cl = FilteredElementCollector(doc)
revs = cl.OfCategory(BuiltInCategory.OST_Revisions).WhereElementIsNotElementType()
for rev in revs:
    print('{0}\tREV#: {1}\tDATE: {2}\tTYPE:{3}\tDESC: {4}'.format(rev.SequenceNumber,
                                                                  str(rev.RevisionNumber).ljust(5),
                                                                  str(rev.RevisionDate).ljust(10),
                                                                  str(rev.NumberType.ToString()).ljust(15),
                                                                  rev.Description))

this_script.output.print_md('*****\n\n\n###REVISED SHEETS:\n')

sheetsnotsorted = FilteredElementCollector(doc).OfCategory(
    BuiltInCategory.OST_Sheets).WhereElementIsNotElementType().ToElements()
sheets = sorted(sheetsnotsorted, key=lambda x: x.SheetNumber)

for sht in sheets:
    revs = sht.GetAllRevisionIds()
    if len(revs) > 0:
        print('{}\t{}\t{}'.format(this_script.output.linkify(sht.Id),
                                  sht.LookupParameter('Sheet Number').AsString(),
                                  sht.LookupParameter('Sheet Name').AsString()))
        for rev in revs:
            rev = doc.GetElement(rev)
            print('\tREV#: {0}\t\tDATE: {1}\t\tDESC:{2}'.format(rev.RevisionNumber,
                                                                rev.RevisionDate,
                                                                rev.Description
                                                                ))
>>>>>>> 48604b4ceb2e8cf57eeca457c1b1250493b5fbd3
