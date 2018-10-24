import pytest

@pytest.fixture
def bamfile():
	return "tests/data/test.bam"

@pytest.fixture
def pe_bamfile():
	return "tests/data/pe.bam"

@pytest.fixture
def unpaired_bamfile():
	return "tests/data/test_unpaired.bam"

def test_bedtools():
	from distutils.spawn import find_executable
	assert find_executable("bedtools")

def test_bamtobed(bamfile):
	from bam2bw.bampipes import bamtobed
	f = open(bamfile)

	f = bamtobed(f)
	lines = [line.strip() for line in f.readlines()]
	assert 15 == len(lines)
	assert "scaffold_1" == lines[0].split("\t")[0]
	assert "+" == lines[0].split("\t")[-1]
	assert "-" == lines[7].split("\t")[-1]
	assert "44760084" == lines[-1].split("\t")[1]
	assert "44760119" == lines[-1].split("\t")[2]

def test_bamtobed_fragment(pe_bamfile):
	from bam2bw.bampipes import bamtobed
	f =  bamtobed(open(pe_bamfile))
	lines = [line.strip() for line in f.readlines()]
	assert int(lines[0].split("\t")[1]) == 92101
	assert int(lines[-1].split("\t")[2]) == 92316

	f =  bamtobed(open(pe_bamfile), fragment=True)
	lines = [line.strip() for line in f.readlines()]
	assert len(lines) == 1
	assert int(lines[0].split("\t")[1]) == 92101
	assert int(lines[0].split("\t")[2]) == 92316

def test_bamtobed_unpaired_fragment(unpaired_bamfile):
	from bam2bw.bampipes import bamtobed
	f =  bamtobed(open(unpaired_bamfile), fragment=True)
	lines = [line.strip() for line in f.readlines()]
	assert len(lines) == 1
	assert int(lines[0].split("\t")[1]) == 22
	assert int(lines[0].split("\t")[2]) == 141
