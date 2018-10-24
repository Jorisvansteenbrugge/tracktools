Overview
========
The bam2bw script converts a BAM file (doesn't have have to be indexed) to a UCSC bigWig file. You can choose to remove or keep duplicates and/or repeats, extend reads to a specific length and choose read-based or genomic fragment-based visualization. 
Internally, it's a simple wrapper around bedtools, samtools and bigToBigWig with pipes.

Prerequisites
============
* bedtools
* samtools
* wigToBigWig

Optional:

* phantompeakqualtools [https://code.google.com/p/phantompeakqualtools/](https://code.google.com/p/phantompeakqualtools/) - to determine fragment size

Installation
============

Specify the location of run_spp.R in bam2b/config.py.

    python setup.py test
    python setup.py install


Usage
=====


    Usage: bam2bw -i <bamfile> -o <bigWigFile> [options]
 
    Options:
      --version   show program's version number and exit
      -h, --help  show this help message and exit
      -i FILE     Input file name (BAM) or - for STDIN
      -o FILE     Output file name (bigWig)
    
      Optional:
        -g FILE   Genome (chrom sizes), when reading from STDIN
        -e SIZE   Extend reads to SIZE or specify 'auto' to determine
        -f        Genomic fragment based
        -s SCALE  Scaling factor
        -c        adjust scale for fragment size and number of total reads to
                  produce coverage per fragment per million total reads per kb
        -D        Keep duplicates (removed by default)
        -R        Keep repeats (removed by default)
