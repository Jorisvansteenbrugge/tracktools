from distutils.core import setup
from setuptools.command.test import test as TestCommand
import sys
from bam2bw.config import VERSION

DESCRIPTION = """
bam2bw - convert BAM files to bigWig files
"""

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup (name = 'bam2bw',
	version = VERSION,
	description = DESCRIPTION,
	author='Simon van Heeringen',
	author_email='s.vanheeringen@ncmls.ru.nl',
	license='MIT',
	packages=[
		'bam2bw'
	],
	scripts=[
		"scripts/bam2bw",
		"scripts/bam2fragmentsize",
	],
	data_files=[],
    tests_require=['pytest'],
    cmdclass = {'test': PyTest},
)
