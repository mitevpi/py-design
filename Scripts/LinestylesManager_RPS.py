import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
from System.Collections.Generic import *

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
uidoc=DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

# Start Transaction
TransactionManager.Instance.EnsureInTransaction(doc)
lineStyle = doc.Settings.Categories.get_Item(BuiltInCategory.OST_Lines)
lineStyleSubTypes = lineStyle.SubCategories
listNames = []
listId = []
for i in lineStyleSubTypes:
name = i.Name
ID = i.Id
listNames.append(name)
listId.append(ID)

# End Transaction
TransactionManager.Instance.TransactionTaskDone()
OUT = list