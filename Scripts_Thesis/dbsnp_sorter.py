#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from collections import defaultdict, namedtuple

IntervalColumns = namedtuple('line', ['chr', 'start', 'end', 'var'])
intervals_list = []

#INTERVALS_BED = "/media/usb/dbsnp_modified.bed"
INTERVALS_VCF = '/media/partition/00-All.vcf'

if INTERVALS_VCF:
    with open(INTERVALS_VCF, "r") as fin:
        for line in fin.readlines():
            line = line.rstrip('\n')
            line = re.split(r'\t+', line.rstrip('\t'))
            if line[1] == 1:
                bed_line = IntervalColumns(*(line[0], line[1], line[1], line[3], line[4]))
                intervals_list.append(bed_line)
else:
    print("ERROR: Provide an interval list (bed format)")

file = open("dbsnp_hg19.bed", "w")

file.write(intervals_list)

file.close()
