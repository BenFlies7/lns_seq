#!usr/bin/env python

"""
This script parses over a FASTQ file, takes the size of each record
puts the sizes into bins according to their length and plots the result

"""

###Input
file_name = raw_input("Filename?\n")

###import modules
from Bio import SeqIO
import pylab as p
import numpy as np

###Parse over the records & take the size of each record
sizes = [len(rec) for rec in SeqIO.parse(file_name, "fastq")]

###Plot
#Define a histogram & put sizes into bins
binsize = max(sizes) / 10
y,binEdges = np.histogram(sizes,binsize)

#Consider only the bin centers
bincenters = 0.5*(binEdges[1:]+binEdges[:-1])

#Align the bin centers
p.plot(bincenters,y,'-')

#p.title("Distribution of Sequence Lengths over all Sequences\n%i Sequences; Lengths %i to %i" %(len(sizes),min(sizes),max(sizes)))
p.xlabel("Read Length (bp)")
p.ylabel("Count")
p.show()
