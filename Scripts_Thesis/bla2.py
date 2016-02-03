#!/usr/bin/python
# -*- coding: utf-8 -*-

#import modules
import os
import pysam
import matplotlib.pyplot as plot
import numpy
import csv

#import bam file and index if necessary
bamfile = pysam.Samfile("read1_trimmed.bam","rb")
if not os.path.exists("read1_trimmed.bam.bai"):
    pysam.index("read1_trimmed.bam")

with open("spam.csv","rb") as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        x = []
        y = []
        for column in bamfile.pileup(str(row[0]),int(row[1]),int(row[2]),max_depth = 1000000):
            x.append(column.pos)
            n = 0
            for read in column.pileups:
                if (not read.is_del):
                    n += 1
                    y.append(n)
            plot.boxplot(x)

plot.figure(figsize=(15, 5))
"""
plot.plot(x, y, 'b')
plot.plot([x[0], x[-1]], [numpy.mean(y[50:-50]), numpy.mean(y[50:-50])], ':r')
plot.show()
"""
plot.show()
