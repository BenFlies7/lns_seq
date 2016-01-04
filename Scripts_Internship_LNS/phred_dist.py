#! usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script calculates the percentage of reads above a certain
threshold for each position and plots the result
"""

#import modules
from Bio import SeqIO
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import pylab as p
import random

### Input
file_name = raw_input("Filename?\n")
threshold_input = raw_input("Enter your threshold list\n")
threshold_list = eval(threshold_input)
thresholds = np.asarray(threshold_list)

### Open file & parse over it
recs = SeqIO.parse(file_name,"fastq")

### Open a default directory d1
d1 = defaultdict(list)

### For each record, put pos + qual into d1
for rec in recs:
        pos = 0
        for i,qual in enumerate(rec.letter_annotations["phred_quality"]):
                pos = i + 1
                d1[pos].append(qual)

### Define the phred score thresholds
d2 = {k:sum(1 for x in v if x) for k,v in d1.items()}

### Define a function to calculate the percentage of reads over the threshold and to plot the result
def ratio(dictionary,threshold):
    count_dict = defaultdict(list)
    count_dict = {k:sum(1 for x in v if x >= threshold) for k,v in dictionary.items()}
    ratio = {k:(count_dict[k] / float(d2[k])) for k in count_dict}
    x = np.arange(len(ratio))
    y = ratio.values()
    color = "#%03x" % random.randint(0, 0xFFFFFF)
    plt.plot(x,y,color, label=threshold)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

### Go over the threshold list & show the result
for index,value in enumerate(thresholds):
    ratio(d1,value)

#plt.title("Distribution of read quality per position passing a certain phred threshold")
plt.xlabel("Read position")
plt.ylabel("Percentage of reads passing the threshold")
p.show()
