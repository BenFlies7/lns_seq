#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import re
import gzip
from Bio import SeqIO

def process(directory):
    for arg in directories:
        os.chdir("/home")
        path_fastq = arg
        os.chdir(os.path.dirname(os.path.abspath(arg)))
        files = os.listdir(path_fastq)
        f = [os.path.join(root,name)
                    for root, dirs, files in os.walk(path_fastq)
                    for name in files
                    if name.endswith((".fastq", ".fastq.gz"))]
        #filelist = os.listdir(directory)
        for file in f:
            handle = gzip.open(file)
            SeqIO.convert(handle, "fastq", handle.replace(".fastq",".fasta"), "fasta", alphabet= IUPAC.ambiguous_dna)

directories = sys.argv[1]

process(directories)
