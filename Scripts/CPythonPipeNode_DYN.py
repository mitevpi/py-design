import sys
sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Lib')
import os
import csv
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

str = IN[0]
working_dir = IN[1]
data_in = IN[2]
var_list = []

#define the output files
script_file = IN[1] + "\PYT3_script.py"
data_file = working_dir + "/data.csv"

#write data in to csv
with open(data_file,'wb') as dataFile:
    wr = csv.writer(dataFile, dialect='excel')
    wr.writerows([data_in])
		
#start stdout for creating a .py from the input "string"
stdsave = sys.stdout
fout = open(script_file,'w')
sys.stdout = fout

#create a results.txt file
result_file = working_dir + "/results.txt"
string_formatted = str.replace("working_directory", working_dir + "\\results.txt")

#write input "string" to .py 
print(string_formatted)
sys.stdout = stdsave
fout.close()

#read input data
with open(data_file) as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		var_list.append(row)

#run .py via CMD instance
pyt3_string = '"cmd.exe /c "cd/DIRECTORY&&python PYT3_script.py"'
pyt3_string_formatted = pyt3_string.replace("DIRECTORY", working_dir)
pyt3_string_formatted2 = pyt3_string_formatted.replace("C:\\", "")

#add a sys path to the created .py directory
os.system(pyt3_string_formatted2)

#define outputs
OUT = script_file, working_dir, result_file, string_formatted, var_list