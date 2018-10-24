import os
import sys
import subprocess as sp
from bam2bw.config import SAMTOOLS
import pysam

def get_total_reads(bamfile):
    if os.path.exists("{0}.bai".format(bamfile)):
        cmd = "{0} idxstats {1} |awk '{{total += $3 + $5}} END {{print total}}'"
        p = sp.Popen(cmd.format(SAMTOOLS, bamfile), shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
        stdout, stderr = p.communicate()
        return int(stdout.strip())
    else:
        sys.stderr.write("Use an indexed bam file for quicker counts!\n")
        cmd = "{0} view {1} | wc -l"
        p = sp.Popen(cmd.format(SAMTOOLS, bamfile), shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
        stdout, stderr = p.communicate()
        return int(stdout.strip())

def split_stranded_bam(inbam, outforward, outreverse, pe=True):
    """ write a BAM file with all reads mapped to plus strand"""
    
    reverse_flags = [99, 147, 1123, 1171]
    forward_flags = [83, 163, 1107, 1187]

    if not pe:
        reverse_flags = [0, 1024]
        forward_flags = [16, 1040]
        
    f = pysam.Samfile(inbam, "rb")
    f_forward = pysam.Samfile(outforward, "wb", template=f)
    f_reverse = pysam.Samfile(outreverse, "wb", template=f)

    for read in f:
        if read.flag in forward_flags:
            f_forward.write(read)
        elif read.flag in reverse_flags:
            f_reverse.write(read)
        
    f.close()
    f_forward.close()
    f_reverse.close()
        

