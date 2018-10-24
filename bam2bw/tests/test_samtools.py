import pytest

@pytest.fixture
def bamfile():
    return "tests/data/test.bam"

def test_samtools():
    from distutils.spawn import find_executable
    assert find_executable("samtools")

def test_makegenome(bamfile):
    from bam2bw.bampipes import genome_from_bamfile
    fname = genome_from_bamfile(bamfile)
    lines = [line.strip() for line in open(fname).readlines()]
    assert 1 == len(lines)
    chrom,length = lines[0].split("\t")
    assert "scaffold_1" == chrom 
    assert "215906545" == length

def test_raise_error_if_not_file_object():
    from bam2bw.bampipes import bamview
    with pytest.raises(TypeError):
        bamview("Im_a_string.bam")

def test_bamview_sam(bamfile):
    from bam2bw.bampipes import bamview
    f = bamview(open(bamfile), bam=False)
    assert 17 == len(f.readlines())

#def test_bamview_pipe(bamfile):
#    from bam2bw.bampipes import bamview

def test_bamview_sam_rmdup(bamfile):
    from bam2bw.bampipes import bamview
    f = bamview(open(bamfile), bam=False, rmdup=True)
    assert 12 == len(f.readlines())

def test_bamview_sam_rmrepeat(bamfile):
    from bam2bw.bampipes import bamview
    f = bamview(open(bamfile), bam=False, rmrepeat=True)
    lines = f.readlines()
    assert 12 == len(lines)

def test_bamview_bam_rmrepeat(bamfile):
    from bam2bw.bampipes import bamview
    f = bamview(open(bamfile), bam=True, rmrepeat=True)
    assert f.read() != None

def test_bamview_sam_rmrepeat_rmdup(bamfile):
    from bam2bw.bampipes import bamview
    f = bamview(open(bamfile), bam=False, rmrepeat=True, rmdup=True)
    assert 7 == len(f.readlines())

def test_bamview_bam(bamfile):
    from bam2bw.bampipes import bamview
    from tempfile import NamedTemporaryFile
    
    # Read BAM file, write to BAM file
    f = bamview(open(bamfile), bam=True)
    tmp = NamedTemporaryFile()
    tmp.write(f.read())
    tmp.flush()
    
    f = bamview(open(tmp.name), bam=False)
    assert 17 == len(f.readlines())
    
