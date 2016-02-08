#!/usr/bin/python
# -*- coding: utf-8 -*-

#import modules
import os
import pysam
import matplotlib.pyplot as plot
import numpy
import csv

#import bam file and index if necessary
bamfile = pysam.AlignmentFile("assembly.bam","rb")

m = []
#"chr1", 115256524, 115256525)
for read in bamfile.fetch("chr1", 115256524 -1 , 115256525 -1):
    qual = read.mapping_quality
    m.append(numpy.mean(qual))

print numpy.mean(m)
