import sys
pyt_path = r'C:\\Program Files (x86)\\IronPython 2.7\\Lib'
sys.path.append(pyt_path)
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

from difflib import SequenceMatcher

dataEnteringNode = IN

sorted_list = []
sorted_detail_list = []
sorted_detail_strings = []
sorted_strings = []
exist_list = []
match_list = []
original_list = IN[0]
detail_list = IN[1]

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

for i in original_list:
    result = sorted(i)
    if result not in sorted_list:
    	sorted_list.append(result)
    else : exist_list.append(i)

for x in detail_list:
    result2 = sorted(x)
    if result2 not in sorted_detail_list:
        sorted_detail_list.append(result2)

sorted_detail_strings = map(IN[2].join, sorted_detail_list)
sorted_strings = map(IN[2].join, sorted_list)

for n in sorted_strings:
	#percent_match = similar(n, sorted_strings)
	#percent_match = map(similar, n, sorted_strings)
    percent_match = [similar(n, x) for x in sorted_detail_strings]
    match_list.append(percent_match)

OUT = sorted_list, exist_list, sorted_detail_strings, sorted_strings, match_list