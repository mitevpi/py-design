import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)
import clr

#random
import random
from random import randint

#Import module for Revit
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

#import module for the Document and transactions
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

#import Revit API
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.DB.Analysis import *

#document
doc = DocumentManager.Instance.CurrentDBDocument
dataEnteringNode = IN
OUT = []