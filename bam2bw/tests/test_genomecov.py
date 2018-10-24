import pytest

@pytest.fixture
def bedfile():
	return "tests/data/test_genomecov.bed"

@pytest.fixture
def genomefile():
	return "tests/data/genome.txt"

def test_bedtools():
	from distutils.spawn import find_executable
	assert find_executable("bedtools")

def test_genomecov(bedfile, genomefile):
	from bam2bw.bampipes import genomecov
	f = open(bedfile)

	f = genomecov(f, genomefile)
	lines = [line.strip() for line in f.readlines()]
	assert 4 == len(lines)
	assert "chr1\t0\t21\t1" == lines[0]
	assert "chr1\t21\t41\t2" == lines[1]
	assert "chr1\t41\t61\t3" == lines[2]
	assert "chr1\t61\t80\t4" == lines[3]

def test_scale(bedfile, genomefile):
	from bam2bw.bampipes import genomecov
	f = open(bedfile)

	f = genomecov(f, genomefile, scale=0.5)
	lines = [line.strip() for line in f.readlines()]
	assert 4 == len(lines)
	assert "chr1\t0\t21\t0.5" == lines[0]
	assert "chr1\t21\t41\t1" == lines[1]
	assert "chr1\t41\t61\t1.5" == lines[2]
	assert "chr1\t61\t80\t2" == lines[3]

def test_reverse(bedfile, genomefile):
	from bam2bw.bampipes import genomecov
	f = open(bedfile)

	f = genomecov(f, genomefile, reverse=True)
	lines = [line.strip() for line in f.readlines()]
	assert 4 == len(lines)
	assert "chr1\t0\t21\t-1" == lines[0]
	assert "chr1\t21\t41\t-2" == lines[1]
	assert "chr1\t41\t61\t-3" == lines[2]
	assert "chr1\t61\t80\t-4" == lines[3]

