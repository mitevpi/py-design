import sys
sys.path.append(r'C:\\Program Files (x86)\\IronPython 2.7\\Lib')
sys.path.append(r'C:\\Users\\584\\AppData\\Roaming\\Dynamo\\Dynamo Revit\\1.3\\packages\\RevitPythonWrapper\\extra\\rpw.zip')
import time
import rpw
from rpw.ui.forms import Console

var1 = 'Test'

for i in range(10):
	if i ==5:
		Console(context=locals())

print('test')
OUT = var1