#!usr/bin/env python
# -*- coding: utf-8 -*-

import pybedtools
import time
import urllib
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec

BAM_file = sys.argv[1]
BED_file = sys.argv[2]

def get_coverage(bam_file,bed_file):
    """
    Compute the coverage from an input BAM file,
    by only taking into consideration the regions
    provided in the BED file. Plot the resulting
    histogram & boxplot.
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
    fig = plt.figure(figsize=(12, 6))
    gs = gridspec.GridSpec(1, 2, width_ratios=[2.5, 1])
    ax1 = plt.subplot(gs[0])
    ax1.set_title("Coverage Histograms")
    bins = len(coverage_array)
    ax1.hist(coverage_array,bins,orientation="horizontal")
    ax1.set_xlabel("Coverage (X)")
    ax1.set_ylabel("Count")
    ax2 = plt.subplot(gs[1])
    ax2.set_title("Coverage Distribution")
    ax2.boxplot(coverage_array)
    ax2.set_ylabel("Coverage (X)")
    plt.show()

get_coverage(BAM_file, BED_file)
