#!usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script sorts all .bam files of a given input directory
"""

import pysam
import sys
import os
import re

def get_basename(name, extensions):
    """
    Extensions: ['.bam']
    Cuts of extensions provided and full path,
    If cut_paired, it looks to detect paired signs and cuts those off
    """
    if name is None:
        return None
    else:
        name = os.path.basename(name)
        for ext in extensions:
            name = re.sub("%s$" % ext, '', name)
        return name

def aligned_counts(ifile1):
    '''count how many alignments are aligned back to genome, ifile1 is a sorted bam file'''
    import HTSeq
    sortedbamfile= HTSeq.BAM_Reader(ifile1)
    aligned_counts=0
    unaligned_counts=0
    for almnt in sortedbamfile:
        if almnt.aligned:
            aligned_counts+= 1
        else:
            unaligned_counts+=1
    sum = float(aligned_counts) + float(unaligned_counts)
    ratio = (aligned_counts / sum) * float(100)
    #print "number of aligned tags of %s is %d " % (ifile1, aligned_counts)
    #print "number of unaligned tags of %s is %d "% (ifile1, unaligned_counts)
    print "percentage of mapped reads is %s"% ratio
    return aligned_counts

directories = sys.argv[1:]

for arg in directories:

    os.chdir("/home")
    path_fastq = arg
    os.chdir(os.path.dirname(os.path.abspath(arg)))
    files = os.listdir(path_fastq)

    #search fastq files:
    f = [os.path.join(root,name)
                 for root, dirs, files in os.walk(path_fastq)
                 for name in files
                 if name.endswith(".bam")]

    for file in f:
        basename = get_basename(file, [".bam"])
        pysam.sort(file,basename+"_sorted")

#aligned_counts("2015-11-1_S1_sorted.bam")
