#!/usr/bin/python
# -*- coding: utf-8 -*-

#import modules
import os
import pysam
import matplotlib.pyplot as plt
import numpy
import csv
import sys
from collections import namedtuple, defaultdict
import re

input_bamfile = sys.argv[1]
INTERVALS = sys.argv[2]

bamfile = pysam.AlignmentFile(input_bamfile, "rb")

IntervalColumns = namedtuple('bed', ['chr', 'start', 'end'])
intervals_list = []
with open(INTERVALS, "r") as fin:
    for line in fin.readlines():
        line = line.rstrip('\n')
        line = re.split(r'\t+', line.rstrip('\t'))
        if len(line) == 3:
            bed_line = IntervalColumns(*line)
            intervals_list.append(bed_line)

quals = []
for interval in intervals_list:
    start = int(interval.start)
    end = int(interval.end)
    length = end - start
    pos_key = "%s:%s:%s" % (interval.chr, interval.start, interval.end)
    for aligned_pos in range(start, start + length):
        for read in bamfile.fetch(reference=interval.chr, start=start, end=end):
            qual = read.mapping_quality
            quals.append(qual)

#print numpy.mean(quals)
plt.hist(quals, bins = 60)
plt.title("Mapping Quality Histograms")
plt.xlabel("Mapping Quality")
plt.ylabel("Count")
plt.show()
