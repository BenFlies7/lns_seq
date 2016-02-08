#!usr/bin/env python
# -*- coding: utf-8 -*-

import pybedtools
import time
import urllib
import sys
import numpy as np
import matplotlib.pyplot as plt

def get_coverage(bam_file,bed_file):
    """
    Compute the coverage from an input BAM file,
    by only taking into consideration the regions
    provided in the BED file.
    """
    almnt = pybedtools.BedTool(bam_file)
    regions = pybedtools.BedTool(bed_file)
    print "Calculating coverage over regions ..."
    sys.stdout.flush()
    t0 = time.time()
    coverage_result = almnt.coverage(regions).sort()
    print coverage_result
    coverage_array = np.array([i[-4] for i in coverage_result], dtype=float)
    print coverage_array
    t1 = time.time()
    print "completed in %.2fs" % (t1-t0)
    sys.stdout.flush()
    bins = len(coverage_array)
    plt.hist(coverage_array,bins)
    plt.show()
    #print coverage_array

get_coverage("/mnt/files-bioseq/bioseq-temporary/ben/Test/assembly.bam", "00100-1407755742_Regions.bed")
