import glob
import sys
import os
import re
import numpy

if len(sys.argv) < 2:
	print(f'ERROR: need to provide fule path to model output files')
	sys.exit(1)

files = glob.glob(sys.argv[1])
steps = []
for f in files:
	fbase = os.path.basename(f)
	m = re.match(r'^model_output_(\d+).txt', fbase)
	if m:
		steps.append( int(m.group(1)) )
	else:
		print(f'cannot parse {fbase}')

# find the largest value
if len(steps) > 0:
	step = numpy.amax(steps)
	print(step)
else:
	# no output file
	print(0)