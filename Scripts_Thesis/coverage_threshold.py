#!usr/bin/env python
# -*- coding: utf-8 -*-

#Load modules
import pybedtools
import re
from collections import namedtuple, defaultdict
import numpy as np
import matplotlib.pyplot as plt


#Load files
BAM_FILE = "/media/partition/Haloplex_Test_1_Late_January/Velona/15038519_S3.bam"
INTERVALS_BED = "/media/partition/Haloplex_Test_1_Late_January/00100-1407755742_Regions.bed"

almnt = pybedtools.BedTool(BAM_FILE)
regions = pybedtools.BedTool(INTERVALS_BED)

IntervalColumns = namedtuple('bed', ['chr', 'start', 'end', 'gene'])
intervals_list = []

def convert_keys_to_string(dictionary):
    """Recursively converts dictionary keys to strings."""
    if not isinstance(dictionary, dict):
        return dictionary
    return dict((str(k), convert_keys_to_string(v))
        for k, v in dictionary.items())

"""
if INTERVALS_BED:
    with open(INTERVALS_BED, "r") as fin:
        for line in fin.readlines():
            line = line.rstrip('\n')
            line = re.split(r'\t+', line.rstrip('\t'))
            prc = ()
            if len(line) == 4:
                line[1] = int(line[1])
                line[2] = int(line[2])
                line[3] = re.sub('_\d$','',line[3])
                bed_line = IntervalColumns(*(line[0], int(line[1]), int(line[2]), line[3]))
                intervals_list.append(bed_line)
else:
    print("ERROR: Provide an interval list (bed format)")
"""

coverage_result = almnt.coverage(regions).sort()

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
