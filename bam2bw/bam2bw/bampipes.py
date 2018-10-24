#!/usr/bin/env python 
# Copyright (c) 2013 Simon van Heeringen <s.vanheeringen@ncmls.ru.nl>
#
# This module is free software. You can redistribute it and/or modify it under 
# the terms of the MIT License, see the file COPYING included with this 
# distribution.

import sys
import os
import subprocess
from tempfile import NamedTemporaryFile
import re
from bam2bw import config as cfg

def genome_from_bamfile(bamfile):
    tmp = NamedTemporaryFile(delete=False)
    cmd = "%s view -H %s" % (cfg.SAMTOOLS, bamfile)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    
    r = re.compile(r'@SQ\s+SN:([!-)+-<>-~][!-~]*)\s+LN:(\d+)')
    for line in p.stdout:
        m = r.search(line)
        if m:
            tmp.write("%s\t%s\n" % (m.group(1), m.group(2)))
    tmp.flush()
    
    return tmp.name

def bamview(fobj, rmdup=False, rmrepeat=False, bam=True, pe=False):
    """
    Takes a filehandle as input and returns a stdout filehandle to bam output
    """
    
    if not hasattr(fobj, "read") or type(fobj) == type(""):
        raise TypeError, "need a file object"
    
    flags = ["-h -F 2048"]
    
    if pe:
        flags.append("-f 3")    # Only properly paired reads

    if rmdup:
        flags.append("-F 1024")

    cmd = "%s view %s -" % (cfg.SAMTOOLS, " ".join(flags))
    if rmrepeat:
        cmd += '| grep -v "XT:A:[^U]"'
        cmd += '| grep -v "NH:i:[2-9]" | grep -v "NH:i:[0-9][0-9]"'
    if bam:
        cmd += '| samtools view -ubS - '

    p = subprocess.Popen(cmd, shell=True, stdin=fobj, stdout=subprocess.PIPE, close_fds=True)
    
    return p.stdout

def bamtobed(fin, fragment=False):
    """  
    Takes BAM-formatted stdin, returns BED-formatted stdout
    """
    if fragment:
        #sys.stderr.write("Fragment mode, please ensure that your BAM file is sorted by name!\n")
        pebed2bed = "awk '{if ($1 == $4 && $1 != \".\") print $1 \"\\t\" $2 \"\\t\" $6}'"
        cmd = "%s bamtobed -bedpe | %s | sort -k1,1" % (
            cfg.BEDTOOLS,
            pebed2bed
        )
    else:
        cmd = "%s bamtobed -split" % cfg.BEDTOOLS
    
    p = subprocess.Popen(cmd, shell=True, stdin=fin, stdout=subprocess.PIPE, close_fds=True)
    return p.stdout

def genomecov(fin, genome, bam=False, scale=1.0, reverse=False):
    """
    Takes a BED- or BAM formatted stdin and returns stdout filehandle to bedgraph output
    """
    
    default = "-i"
    if bam:
        default = "-ibam"

    process = ""
    if reverse:
        process = " | perl -ple 's/(\d+(\.\d+)?(e[+-]\d+)?)$/-\\1/'"
    
    cmd = "{0} genomecov -scale {1} -split -bg {2} - -g {3} {4}".format(
                                                        cfg.BEDTOOLS, 
                                                        scale,
                                                        default, 
                                                        genome,
                                                        process,
                                                        )
    
    p = subprocess.Popen(cmd, shell=True, stdin=fin, stdout=subprocess.PIPE, close_fds=True)
    
    # This actually only works if there is something printed to stderr, otherwise it blocks
    #err_line = p.stderr.readline().strip()
    #if err_line.endswith("not sorted correctly."):
    #    raise Exception, "Whoa! I think your input is not sorted by position!"
    return p.stdout

def extendbed(fin, extend=0):
    cmd = 'awk \'{if ($6 == "-") $2 = $3 - %s; else $3 = $2 + %s}1\' | ' % (extend, extend)
    cmd += 'awk \'{if ($2 < 0) $2 = 0}1\' | tr \\  \\\\t'
    
    p = subprocess.Popen(cmd, shell=True, stdin=fin, stdout=subprocess.PIPE, close_fds=True)
    
    return p.stdout

def makebigwig(fin, fname, genome):
    """
    Takes BED- or Wiggle-formatted stdin and writes to a bigWig file
    """
    cmd = "%s /dev/stdin %s %s -clip" % (cfg.WIG2BIGWIG, genome, fname)
    p = subprocess.call(cmd, shell=True, stdin=fin, close_fds=True)
