#!/usr/bin/env python
"""
This module transforms the hw3 results into three different 
result files for later steps.
'results.eval' --> 
1) q1_hw3_result.eval
2) q2_hw3_result.eval
3) q3_hw3_result.eval
"""

import sys
import os

if (len(sys.argv) != 2):
    print("ERROR: please include the path to the results file as param")
    exit(1)
directory = "outputs/"
if not os.path.exists(directory):
    os.makedirs(directory)
result = open(sys.argv[1], 'r')
q1 = open(directory + "q1_hw3_result.eval", "w")
q2 = open(directory + "q2_hw3_result.eval", "w")
q3 = open(directory + "q3_hw3_result.eval", "w")
# The first three queries' results
for line in result:
    if line[0] == '1':
        q1.write(line)
    elif line[0] == '2':
        q2.write(line)
    elif line[0] == '3':
        q3.write(line)
result.close()
q1.close()
q2.close()
q3.close()
