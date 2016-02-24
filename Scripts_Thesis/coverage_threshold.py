#!usr/bin/env python
# -*- coding: utf-8 -*-

#Load modules
import pybedtools
import re
import sys
from collections import namedtuple, defaultdict
import numpy as np
import matplotlib.pyplot as plt


#Load files
BAM_FILE = "/media/partition/Haloplex_Test_1_Late_January/Velona/15061857_S2.bam"
INTERVALS_BED = "/media/partition/Haloplex_Test_1_Late_January/00100-1407755742_Regions.bed"

COVERAGE_THRESHOLD = 2000

almnt = pybedtools.BedTool(BAM_FILE)
#regions = pybedtools.BedTool(INTERVALS_BED)

IntervalColumns = namedtuple('bed', ['chr', 'start', 'end', 'gene'])
intervals_list = []


if sys.argv[1] == 'all':
    if INTERVALS_BED:
        with open(INTERVALS_BED, "r") as fin:
            for line in fin.readlines():
                line = line.rstrip('\n')
                line = re.split(r'\t+', line.rstrip('\t'))
                if len(line) == 4:
                    line[1] = int(line[1])
                    line[2] = int(line[2])
                    line[3] = re.sub('_\d$','',line[3])
                    bed_line = IntervalColumns(*(line[0], int(line[1]), int(line[2]), line[3]))
                    intervals_list.append(bed_line)
    else:
        print("ERROR: Provide an interval list (bed format)")
elif sys.argv[1] == 'interest':
    if INTERVALS_BED:
        with open(INTERVALS_BED, "r") as fin:
            for line in fin.readlines():
                line = line.rstrip('\n')
                line = re.split(r'\t+', line.rstrip('\t'))
                if len(line) == 4:
                    if (re.sub('_\d$','',line[3]) == 'EGFR') \
                    or (re.sub('_\d$','',line[3]) == 'KRAS') \
                    or (re.sub('_\d$','',line[3]) == 'NRAS') \
                    or (re.sub('_\d$','',line[3]) == 'BRAF'):
                        line[1] = int(line[1])
                        line[2] = int(line[2])
                        #line[3] = re.sub('_\d$','',line[3])
                        bed_line = IntervalColumns(*(line[0], int(line[1]), int(line[2]), line[3]))
                        intervals_list.append(bed_line)
    else:
        print("ERROR: Provide an interval list (bed format)")

coverage_result = almnt.coverage(intervals_list).sort()

coverage_list = []
names = []

for interval in coverage_result:
    coverage_list.append(interval[4])
    names.append(interval[3])
    if float(interval[4]) <=1:
        print('Amplicon %s was not amplified at all !' %interval[3])
    elif 1 < float(interval[4]) <= COVERAGE_THRESHOLD:
        print('Amplicon %s was not amplified efficiently (coverage: %s x)' %(interval[3], interval[4]))

coverage_list = np.asarray(coverage_list).astype(np.float)
N = len(coverage_list)
x = range(N)
plt.bar(x,coverage_list)
plt.axhline(y=1000, color = 'r')
plt.xticks(x, names,rotation='vertical', fontsize = 7)
#plt.xticks(x, names)

plt.show()



"""
collected = defaultdict(list)
for interval in coverage_result:
    interval[3] = re.sub('_(\d+)$','',interval[3])
    if interval[3] not in collected:
        collected[interval[3].encode('ascii','ignore')] = {
        "coverage" : [interval[4].encode('ascii','ignore')]
        }
    else:
        collected = convert_keys_to_string(collected)
        collected[interval[3]]['coverage'].append(interval[4].encode('ascii','ignore'))
print(collected)

for k,v in collected.items():
    data = v['coverage']
    plt.hist(data,sym='')
plt.show()
"""
