#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from collections import defaultdict

#IntervalColumns = namedtuple('line', ['chr', 'start', 'end', 'var'])
#intervals_list = []

INTERVALS_BED = "/media/usb/dbsnp_modified.bed"
INTERVALS_VCF = '/media/partition/hg19/dbsnp_138.hg19.vcf'

'''
with open('dbsnp_output.bed',"w") as f_out:
    if INTERVALS_BED:
        with open(INTE    if INTERVALS_BED:
        with open(INTERVALS_BED, "r") as fin:
            for line in fin.readlines():
                line = line.rstrip('\n')
                line = re.split(r'\t+', line.rstrip('\t'))
                line[0] = re.sub("chr", '', line[0])
                line[8]= re.split(r'/',line[8].rstrip('/'))
                bed_line = IntervalColumns(*(line[0], float(line[1]), float(line[2]), line[8]))
                intervals_list.append(bed_line)
    else:
        print("ERROR: Provide an interval list (bed format)") line.rstrip('\n')
                line = re.split(r'\t+', line.rstrip('\t'))
                line[0] = re.sub("chr", '', line[0])
                line[8]= re.split(r'/',line[8].rstrip('/'))
                bed_line = IntervalColumns(*(line[0], float(line[1]), float(line[2]), line[8]))
                intervals_list.append(bed_line)
    else:
        print("ERROR: Provide an interval list (bed format)")

    for row in intervals_list:
        f_out.write(intervals_list[row])
'''

'''
collected = {}

with open(INTERVALS_BED, "r") as fin:
    alt = 0
    ref = 0
    for line in fin.readlines():
        line = line.rstrip('\n')
        line = re.split(r'\t+', line.rstrip('\t'))
        line[0] = re.sub("chr", '', line[0])
        line[2] = float(line[2])-1
        line[-2] = line[8].split("/")[0]
        line[-1] = line[8].split("/")[1]
        #collected[line] = {
        #    'chr' : float(line[0]),
        #    'start' : float(line[1]),
        #    'end' : float(line[2])-1,
        #    'var' : line[8]
        #}
        print line
'''
if INTERVALS_VCF:
    with open(INTERVALS_VCF, "r") as fin:
        for line in fin.readlines():
            line = line.rstrip('\n')
            line = re.split(r'\t+', line.rstrip('\t'))
            if len(line) == 8:
                line[0] = re.sub("chr", '', line[0])
                bed_line = IntervalColumns(*(line[0], float(line[1]), float(line[1]), line[3], line[4]))
                intervals_list.append(bed_line)
else:
    print("ERROR: Provide an interval list (bed format)")

print intervals_list
