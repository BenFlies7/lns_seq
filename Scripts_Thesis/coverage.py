#!usr/bin/env Python
import pysam

#First import the bam file
bamfile = pysam.Samfile("2015-11-1_S1.bam", "rb")

cov = count_coverage(bamfile,"chr12",25204789,25250938)
print(cov)

"""
# You can now iterate over the bamfile object as:

for pileup in bamfile.pileup("chr12", truncate=True):
  print pileup.n

#This will print out the coverage of the position 10000-10020 in the name "Chr4"
#If you want entire Chr4 you simply write:

for pileup in bamfile.pileup("chr12",25204789,25250938):
  print pileup.n

# The position of each base can be called with pileup.pos

# If you want to iterate over the entire bamfile a good thing could be to get a tuple with all headers:

headers = bamfile.references

# Or you can get a dictionary including also the length of each name:

header_dict = bamfile.header
"""
