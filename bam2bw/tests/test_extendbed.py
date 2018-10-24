import pytest

@pytest.fixture
def bedfile():
	return "tests/data/test_extend.bed"

def test_extendbed(bedfile):
	from bam2bw.bampipes import extendbed
	f = open(bedfile)
	f = extendbed(f, 300)
	lines = [line.strip() for line in f]
	assert len(lines) == 4
	assert lines[0] == "chr1\t100\t400\t.\t.\t+"
	assert lines[1] == "chr1\t100\t400\t.\t.\t-"
	assert lines[2] == "chr1\t10\t310\t.\t.\t+"
	assert lines[3] == "chr1\t0\t10\t.\t.\t-"
