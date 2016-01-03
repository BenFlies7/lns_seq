#!/usr/bin/python
# -*- coding: utf-8 -*-

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

    size_list = []

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
        sizes = 0
        reads = 0
        for rec in SeqIO.parse(handle, "fastq"):
            reads += 1
            size = len(rec)
            sizes += len(rec)
            size_list.append(size)

    boxes.append(size_list)
    #plt.plot(n.average(av_list),color='w', marker='*', markeredgecolor='k')

plt.boxplot(boxes,sym='')

ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
               alpha=0.5)

#ax1.set_title('Comparison of Read Lengthso \nAcross Each Run (Dec 14 - Nov 15)')
ax1.set_ylabel('Read Length (bp)')

xtickNames = plt.setp(ax1, xticklabels = ['Dec 14','Jan 15', 'Feb 15', 'Mar 15', 'Apr 15', 'May 15', 'Jun 15', 'Jul 15', 'Aug 15', 'Sep 15', 'Oct 15', 'Nov15'])
plt.setp(xtickNames, rotation=45, fontsize=12)

plt.show()
