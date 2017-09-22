#import sys
import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

#import module for Revit
import clr
clr.AddReference("RevitNodes")
clr.AddReference('ProtoGeometry')
clr.AddReference("RevitServices")
clr.AddReference('RevitAPI')
clr.ImportExtensions(Revit.Elements)

#import DesignScript
from Autodesk.DesignScript.Geometry import *
import Revit

#import module for the Document and transactions
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

#import Revit API
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.DB.Analysis import *

#document
doc = DocumentManager.Instance.CurrentDBDocument

#Dynamo
dataEnteringNode = IN
OUT = []