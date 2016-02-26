#!usr/bin/env python
# -*- coding: utf-8 -*-

#Load modules
import pybedtools
import re
import sys
import glob
from collections import namedtuple, defaultdict, OrderedDict
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter



#Load files
#BAM_FILE = "/media/partition/Haloplex_Test_1_Late_January/Velona/15061857_S2.bam"
INTERVALS_BED = "/media/partition/Haloplex_Test_1_Late_January/00100-1407755742_Regions.bed"

#BAM_FILE = "/media/partition/Haloplex_Test_2_Mid_February/Velona/15028422_S6.bam"
#BAM_FILE = "/media/partition/Haloplex_Test_2_Mid_February/Velona/ECD_S9.bam"
#BAM_FILE = "/media/partition/Haloplex_Test_2_Mid_February/Velona/15051669_S1.bam"
#BAM_FILE = "/media/partition/Haloplex_Test_2_Mid_February/Velona/15020056_S2.bam"
#BAM_FILE = "/media/partition/Haloplex_Test_2_Mid_February/Velona/15010800_S3.bam"
#BAM_FILE = "/media/partition/Haloplex_Test_2_Mid_February/Velona/15039121_S7.bam"

#BAM_FILE = "/media/partition/TST15_Test_1_Early_February/Base_Space/BRAF_15018040/Libraries/15018040_S1.bam"
#INTERVALS_BED = "/media/partition/TST15_Test_1_Early_February/TST_15-A-manifest.bed"

COVERAGE_THRESHOLD = 1000

directory = '/media/partition/Haloplex_Test_1_Late_January/Velona/'

fig,ax1 = plt.subplots()
plt.hold = True
boxes = []

bam_file_list = [f for f in glob.iglob(directory+"/*.bam")]

collected = defaultdict(list)

for file in bam_file_list:

    almnt = pybedtools.BedTool(file)

    IntervalColumns = namedtuple('bed', ['chr', 'start', 'end', 'gene'])
    intervals_list = []

    if INTERVALS_BED:
        with open(INTERVALS_BED, "r") as fin:
            for line in fin.readlines():
                line = line.rstrip('\n')
                line = re.split(r'\t+', line.rstrip('\t'))

                # For Agilent Haloplex BED files
                if len(line) == 4:
                    line[1] = int(line[1])
                    line[2] = int(line[2])
                    bed_line = IntervalColumns(*(line[0], int(line[1]), int(line[2]), line[3]))
                    intervals_list.append(bed_line)

                # For Illumina Trusight Tumor 15 BED files
                if len(line) == 12:
                    line[1] = int(line[1])
                    line[2] = int(line[2])
                    bed_line = IntervalColumns(*(line[0], int(line[1]), int(line[2]), line[3]))
                    intervals_list.append(bed_line)
    else:
        print("ERROR: Provide an interval list (bed format)")

    coverage_result = almnt.coverage(intervals_list).sort()

    '''
    Print amplicons that have not been amplified at all
    and amplicons that have coverage < 1000x
    '''
    print('\nFile: %s \n' %file)
    for interval in coverage_result:
        collected[interval[3].encode('ascii','ignore')].append(float(interval[4]))
        if float(interval[4]) <=1:
            print('Amplicon %s was not amplified at all !' %(interval[3]))
        elif 1 < float(interval[4]) <= COVERAGE_THRESHOLD:
            print('Amplicon %s was not amplified efficiently (coverage: %s x)' %(interval[3], interval[4]))
    print('\n#####################################\n')

boxes = []
for key, value in collected.items():
    cov_list = []
    for v in value:
        cov_list.append(v)
    boxes.append(cov_list)
plt.boxplot(boxes)
plt.show()

'''
coverage_list = []
names = []

collected = defaultdict(list)

for interval in coverage_result:
coverage_list.append(interval[4])
names.append(interval[3])
if float(interval[4]) <=1:
    print('Amplicon %s was not amplified at all !' %interval[3])
elif 1 < float(interval[4]) <= COVERAGE_THRESHOLD:
    print('Amplicon %s was not amplified efficiently (coverage: %s x)' %(interval[3], interval[4]))
name = interval[3]
cov = float(interval[4])
collected[name.encode('ascii','ignore')].append(cov)

coverage_list = np.asarray(coverage_list).astype(np.float)
coverage_sorted = OrderedDict(sorted(collected.items(), key = itemgetter(1)))
coverage_list.sort()
N = len(coverage_list)
x = range(N)
plt.bar(x, coverage_list)
plt.xticks(x, coverage_sorted.keys(),rotation='vertical', fontsize = 7)
plt.axhline(y=1000, color = 'r')
plt.ylabel('Coverage (x)')
plt.title('Comparison of Amplicon Depths')
plt.show()
'''