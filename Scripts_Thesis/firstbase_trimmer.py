#!usr/bin/env python
# -*- coding: utf-8 -*-

from Bio import SeqIO
import sys
import os
import re
import gzip

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

for arg in directories:

    os.chdir("/home")
    path_fastq = arg
    os.chdir(os.path.dirname(os.path.abspath(arg)))
    files = os.listdir(path_fastq)

    output_name = "trimmed.fastq.gz"

    #search fastq files:
    f = [os.path.join(root,name)
                 for root, dirs, files in os.walk(path_fastq)
                 for name in files
                 if name.endswith(("R2_001.fastq", "R2_001.fastq.gz"))]

    for file in f:
        handle = gzip.open(file)
        name = get_basename(file,['.fastq', '.fastq.gz'])
        trimmed_reads = (rec[1:] for rec in SeqIO.parse(handle, "fastq"))
        count = SeqIO.write(trimmed_reads, name + "_firstbase_trimmed.fastq", "fastq")
        """
        print("Saved %i reads" % count)
        output=gzip.compress("firstbase_trimmed.fastq")
        """
        #with gzip.open(os.path.join(path_fastq,output_name),"wb") as output:
        #    output.write(trimmed_reads)
        #Zipping does not work yet... you have to do it manually via command line
        
