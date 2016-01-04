#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This script computes boxplots of the quality distribution
of each FASTQ file.
"""

from __future__ import absolute_import, division, print_function
import sys
import os
import gzip
import re
import operator
import numpy as n
import pylab as p
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from Bio import SeqIO

def get_basename(name, extensions, cut_paired=False):
     """
     Extensions: ['.fastq', '.fastq.gz']
     Cuts of extensions provided and full path,
     If cut_paired, it looks to detect paired signs and cuts those off
     """

     if name is None:
          return None
     else:
          name = os.path.basename(name)
          for ext in extensions:
                name = re.sub("%s$" % ext, '', name)
          if cut_paired is True:
                name = re.sub("_L001_R._001$", '', name)
                name = re.sub("_1$|_2$", '', name)
          return name

directories = sys.argv[1:]

fig,ax1 = plt.subplots()
plt.hold = True
boxes = []

for arg in directories:

    os.chdir("/home")
    path_fastq = arg
    os.chdir(os.path.dirname(os.path.abspath(arg)))
    files = os.listdir(path_fastq)

    #search fastq files:
    f = [os.path.join(root,name)
                 for root, dirs, files in os.walk(path_fastq)
                 for name in files
                 if name.endswith((".fastq", ".fastq.gz"))]

    f.sort()

    collected = {}

    for file in f:
        basename = get_basename(file, ['.fastq', '.fastq.gz'], cut_paired=True)
        av_list = []
        handle = gzip.open(file)
        av = 0
        reads = 0
        for rec in SeqIO.parse(handle, "fastq"):
            reads += 1
            count_qual = 0
            for qual in rec.letter_annotations["phred_quality"]:
                count_qual += qual
            if len(rec) > 0:
                average = count_qual / len(rec)

            av_list.append(average)

        boxes.append(av_list)

plt.boxplot(boxes,sym='')

ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)

#ax1.set_title('Comparison of Read Qualities Per FASTQ File')
ax1.set_ylabel('Phred Score')
xtickNames = plt.setp(ax1, xticklabels = ['S1 forward','S1 reverse','S2 forward','S2 reverse','S3 forward','S3 reverse','S4 forward','S4 reverse','S5 forward','S5 reverse','S6 forward','S6 reverse','S7 forward','S7 reverse'])
plt.setp(xtickNames, rotation=45, fontsize=10)

plt.show()
