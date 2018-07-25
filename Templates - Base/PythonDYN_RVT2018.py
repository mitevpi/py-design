#import sys
import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

#import module for Revit
import clr
clr.AddReference('ProtoGeometry')
clr.AddReference('RevitServices')
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')

#RevitServices
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

from System import *
from Autodesk.DesignScript.Geometry import *

#import Revit API
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.DB.Analysis import *

#document
doc = DocumentManager.Instance.CurrentDBDocument

#The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN

#Assign your output to the OUT variable.
OUT = 0