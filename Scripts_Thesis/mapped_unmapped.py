#!/usr/bin/python
# -*- coding: utf-8 -*-

#import modules
from collections import namedtuple
import pysam
import re
import matplotlib.pyplot as plt
import numpy as np

#Load files
REFERENCE = "/media/partition/hg19/ucsc.hg19.fasta"
BAM_FILE = "/media/partition/Haloplex_Test_1_Late_January/Velona/15038519_S3.bam"
INTERVALS_BED = "/media/partition/Haloplex_Test_1_Late_January/00100-1407755742_Regions.bed"

IntervalColumns = namedtuple('bed', ['chr', 'start', 'end'])
intervals_list = []

if INTERVALS_BED:
    with open(INTERVALS_BED, "r") as fin:
        for line in fin.readlines():
            line = line.rstrip('\n')
            line = re.split(r'\t+', line.rstrip('\t'))
            prc = ()
            if len(line) == 4:
                line[1] = int(line[1])
                line[2] = int(line[2])
                bed_line = IntervalColumns(*(line[0], int(line[1]), int(line[2])))
                intervals_list.append(bed_line)
else:
    print("ERROR: Provide an interval list (bed format)")

samfile = pysam.AlignmentFile(BAM_FILE, "rb")
total_mapped = samfile.count('chr7', 1, 159138663)
chr_lengths = samfile.lengths
chr_list = samfile.references
chr_list = ['chrM','chr1', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7', 'chr8', 'chr9', 'chr10', 'chr11', 'chr12', 'chr13', 'chr14', 'chr15', 'chr16', 'chr17', 'chr18', 'chr19', 'chr20', 'chr21', 'chr22', 'chrX', 'chrY']

total_mapped_list = []
chr_mapped_list = []

for i, chr in enumerate(chr_list):
    chr_mapped_counter = 0
    total_mapped = samfile.count(chr_list[i], 1, chr_lengths[i])
    total_mapped_list.append(total_mapped)
    #print(total_mapped)
    for interval in intervals_list:
        if chr == interval.chr:
            chr_mapped = samfile.count(interval.chr, interval.start, interval.end)
            chr_mapped_counter += chr_mapped
    chr_mapped_list.append(chr_mapped_counter)
    print('%s : total mapped %s ; mapped in regions %s'  %(chr, total_mapped, chr_mapped_counter))

fig, ax = plt.subplots()
ind = np.arange(len(chr_list))
width = 0.35
total_map = ax.bar(ind, total_mapped_list, color = 'r')
chr_map = ax.bar(ind + width, chr_mapped_list, color = 'b')

ax.set_ylabel('Reads')
ax.set_title('Comparison of total mapped reads \n per chromosome and mapped reads in regions')
ax.set_xticks(ind + width + width)
ax.set_xticklabels(chr_list)

plt.show()
