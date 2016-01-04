#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This script computes boxplots of the quality distribution across several runs
"""

from __future__ import absolute_import, division, print_function

import sys
import os
import gzip
import csv
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

    av_list = []

    os.chdir("/home")
    path_fastq = arg
    os.chdir(os.path.dirname(os.path.abspath(arg)))
    files = os.listdir(path_fastq)

    #search fastq files:
    f = [os.path.join(root,name)
                 for root, dirs, files in os.walk(path_fastq)
                 for name in files
                 if name.endswith((".fastq", ".fastq.gz"))]

    for file in f:

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
            else:
                average = 0
            if average > 0:
                av += average
            else:
                av = 0

        if reads > 0:
            if average > 0:
                average_qual = av / reads
            else:
                average_qual = 0
        else:
            average_qual = 0

        av_list.append(average_qual)

    boxes.append(av_list)

plt.boxplot(boxes)

ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
               alpha=0.5)

#ax1.set_title('Comparison of Average Read Qualities Per Patient \nAcross Each Run (Dec 14 - Nov 15)')
ax1.set_ylabel('Phred Score')

xtickNames = plt.setp(ax1, xticklabels = ['Dec 14','Jan 15', 'Feb 15', 'Mar 15', 'Apr 15', 'May 15', 'Jun 15', 'Jul 15', 'Aug 15', 'Sep 15', 'Oct 15', 'Nov15'])
plt.setp(xtickNames, rotation=45, fontsize=12)

plt.show()
