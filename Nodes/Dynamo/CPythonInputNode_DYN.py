#!/usr/bin/env python3
#!/bin/bash

import sys
import numpy
import scipy
import csv
from scipy.spatial import distance

var_list = []
num_list = []
data_file = (r'C:\\Users\\584\\data.csv')

with open(data_file) as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		var_list.append(row)

for i in var_list:
    result = list(map(int, i))
    num_list.append(result)

stdsave = sys.stdout
results_file = (r'working_directory')
fout = open(results_file,'w')
sys.stdout = fout

print(num_list)
sys.stdout = stdsave

fout.close()