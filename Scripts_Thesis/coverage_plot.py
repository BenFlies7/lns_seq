#!/usr/bin/python
# -*- coding: utf-8 -*-

#import modules
import os
import pysam

#import bam file and index if necessary
bamfile = pysam.Samfile("read1_trimmed.bam","rb")
if not os.path.exists("read1_trimmed.bam.bai"):
    pysam.index("read1_trimmed.bam")
"""
#count reads
sizeCount = {}
for read in bamfile.fetch():
    sizeCount[len(read.seq)] = sizeCount.get(len(read.seq), 0) + 1

N = 0
for key, count in sizeCount.iteritems():
    N += count
print "Total: %d reads" % N

print bamfile.references
print bamfile.lengths

N = 0
for read in bamfile.fetch("chr7", 55241674,55241712):
    N += 1
print N, "reads in region"
"""
import matplotlib.pyplot as plot
import numpy

x = []
y = []

for column in bamfile.pileup("chr7", 55242415, 55242515, max_depth = 1000000):
    x.append(column.pos)
    n = 0
    for read in column.pileups:
        if (not read.is_del):
            n += 1
    y.append(n)
plot.figure(figsize=(15, 5))
plot.plot(x, y, 'b')
plot.plot([x[0], x[-1]], [numpy.mean(y[50:-50]), numpy.mean(y[50:-50])], ':r')
plot.show()
"""
plot.boxplot(y)
plot.show()
"""
