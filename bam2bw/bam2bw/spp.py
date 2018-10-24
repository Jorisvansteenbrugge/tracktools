import os 
import re
import sys
import subprocess as sp
import tempfile as tf
import pysam

from bam2bw import config as cfg
from bam2bw.util import get_total_reads

def get_fragmentsize(bamfile, subset=1000000, run_spp="run_spp.R"):
    """ Use spp (phantompeakqualtools) to determine fragment size"""


    tmpdir = tf.mkdtemp(prefix="bam2bw")
    # Create tagfile, filtered for dups and multimapped reads
    cmd = "{0} view -F 0x0204 -o - {1}  {2}| {3} awk \'BEGIN{{OFS=\"\\t\"}}{{if (and($2,16) > 0) {{print $3,($4-1),($4-1+length($10)),\"N\",\"1000\",\"-\"}} else {{print $3,($4-1),($4-1+length($10)),\"N\",\"1000\",\"+\"}} }}\' | gzip -c > {4}"
    
    nreads = ""
    view = ""
    
    if subset:
        if get_total_reads(bamfile) > subset: 
            # See if the largest chromosome contains enough reads
            samfile = pysam.Samfile(bamfile,"rb")
            largest = sorted(samfile.header['SQ'], cmp=lambda x,y: cmp(y['LN'], x['LN']))[0]
            chrom_l, size_l = largest['SN'], largest['LN']
            count_l = samfile.count(chrom_l, int(size_l * 0.25), size_l)
            if count_l > subset:
                view = "{0}:{1}-{2}".format(chrom_l, int(size_l * 0.25), size_l)
                nreads = "head -n {0} | ".format(subset)
            else:
                nreads = "head -n {0} | ".format(subset)
    
    tagfile = os.path.join(tmpdir, "bam2bw.tagAlign.gz")
    #print cmd.format(cfg.SAMTOOLS, bamfile, view, nreads, tagfile) 
    sp.call(cmd.format(cfg.SAMTOOLS, bamfile, view, nreads, tagfile), shell=True)
    
    
    # Run spp
    outfile = os.path.join(tmpdir, "tagalign.out")
    pdffile = os.path.join(tmpdir, "bam2bw.tagAlign.pdf")
   
    cmd = "Rscript {0} -c={1} -savp -out={2}"
    
    p = sp.Popen(cmd.format(cfg.SPP, tagfile, outfile), shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    stdout,stderr = p.communicate()
    
    if not os.path.exists(outfile) and stderr:
        sys.stderr.write("{0}\n".format(stderr))
        m = re.compile(r'Error in library.spp.').search(stderr)
        if m:
            sys.stderr.write("Please install spp for R: http://compbio.med.harvard.edu/Supplements/ChIP-seq/\n")
        sys.exit(1)

    # Read output
    line = open(outfile).readline()
    vals = line.strip().split("\t")
    sizes = [int(x) for x in vals[2].split(",")]
    
    # Remove temporary files
    os.remove(tagfile)
    os.remove(outfile)
    os.remove(pdffile)
    os.rmdir(tmpdir)

    for size in sizes:
        if size > 0:
            return size
    
    sys.stderr.write("Fragment size could not be estimated!")
    sys.exit(1)
