#!usr/bin/env python
# -*- coding: utf-8 -*-

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
                 if name.endswith(("R2_L001.fastq", "R2_L001.fastq.gz"))]

from Bio import SeqIO
trimmed_primer_reads = (rec[1:] for rec in \
                        SeqIO.parse("SRR020192.fastq", "fastq"))
count = SeqIO.write(trimmed_primer_reads, "with_primer_trimmed.fastq", "fastq")
print("Saved %i reads" % count)
