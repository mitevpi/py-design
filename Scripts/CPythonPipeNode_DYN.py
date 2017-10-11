import sys
sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Lib')
import os
import csv
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
clr.AddReference('RevitNodes')
clr.AddReference('RevitServices')
clr.AddReference('RevitAPI')

str = IN[0]
working_dir = IN[1]
data_in = IN[2]
var_list = []

script_file = IN[1] + "\PYT3_script.py"
data_file = working_dir + "/data.csv"
		
#start stdout
stdsave = sys.stdout
fout = open(script_file,'w')
sys.stdout = fout

result_file = working_dir + "/results.txt"
string_formatted = str.replace("working_directory", working_dir + "\\results.txt")

print(string_formatted)
sys.stdout = stdsave
fout.close()

#read input data
with open(data_file) as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		var_list.append(row)

#put directory parameter in
pyt3_string = '"cmd.exe /c "cd/DIRECTORY&&python PYT3_script.py"'
pyt3_string_formatted = pyt3_string.replace("DIRECTORY", working_dir)
pyt3_string_formatted2 = pyt3_string_formatted.replace("C:\\", "")

os.system(pyt3_string_formatted2)

OUT = script_file, working_dir, result_file, string_formatted, var_list