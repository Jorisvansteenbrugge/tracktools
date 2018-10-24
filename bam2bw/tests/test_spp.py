import pytest

@pytest.fixture
def bamfile():
	return "tests/data/fragmentsize.bam"

def test_spp_fragment_size(bamfile):
	from bam2bw.spp import get_fragmentsize
	assert 180 == get_fragmentsize(bamfile)

