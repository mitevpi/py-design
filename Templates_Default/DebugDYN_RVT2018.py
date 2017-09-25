import sys
sys.path.append(r'C:\\Program Files (x86)\\IronPython 2.7\\Lib')
import time
stdsave = sys.stdout
fout = open(r'C:\\Users\\584\\output.txt','w')
sys.stdout = fout
t1 = time.time()
duration = time.time() - t1
print('Finished in {} seconds'.format(duration))
sys.stdout = stdsave
fout.close()