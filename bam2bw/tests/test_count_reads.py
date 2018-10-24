import pytest

@pytest.fixture
def bamfile():
	return "tests/data/fragmentsize.bam"

@pytest.fixture
def indexed_bamfile():
    return "tests/data/paired.sorted.pos.bam"

def test_count_bamfile(bamfile):
	from bam2bw.util import get_total_reads
	assert 10000 == get_total_reads(bamfile)

def test_count_indexed_bamfile(indexed_bamfile):
	from bam2bw.util import get_total_reads
	assert 1000 == get_total_reads(indexed_bamfile)
