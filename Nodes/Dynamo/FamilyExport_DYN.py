import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

import datetime
start_time = datetime.datetime.now()

clr.AddReference('RevitAPI')
import Autodesk

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument

trans = TransactionManager.Instance
trans.ForceCloseTransaction()

fams = IN[0]
paths = IN[1]

fams = map(UnwrapElement, fams)

for i in xrange(len(fams) ):
	try:
		famDoc = doc.EditFamily(fams[i])
		famDoc.SaveAs(paths[i])
		famDoc.Close(False)
	except:
		pass

end_time = datetime.datetime.now()

OUT = start_time, end_time