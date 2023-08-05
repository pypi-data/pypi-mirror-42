#!/usr/bin/env python
# -*- coding: utf-8 -*-

# (c) 2015-2018, ETH Zurich, Institut fuer Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

import re
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import sys
if sys.version_info < (3, 5):
    raise 'must use Python version 3.5 or higher'

README = """TBModels is a tool for reading, creating and modifying tight-binding models."""

with open('./tbmodels/__init__.py', 'r') as f:
    MATCH_EXPR = "__version__[^'\"]+(['\"])([^'\"]+)"
    VERSION = re.search(MATCH_EXPR, f.read()).group(2).strip()

EXTRAS_REQUIRE = {
    'kwant': ['kwant'],
    'dev': [
        'pytest', 'pytest-cov', 'yapf==0.24', 'pythtb', 'pre-commit', 'sphinx', 'sphinx-rtd-theme==0.2.4',
        'ipython>=6.2', 'sphinx-click', 'prospector==1.1.6.*', 'pylint==2.1.*'
    ]
}
EXTRAS_REQUIRE['dev'] += EXTRAS_REQUIRE['kwant']

setup(
    name='tbmodels',
    version=VERSION,
    url='http://z2pack.ethz.ch/tbmodels',
    author='Dominik Gresch',
    author_email='greschd@gmx.ch',
    description='Reading, creating and modifying tight-binding models.',
    install_requires=[
        'numpy', 'scipy>=0.14', 'h5py', 'fsc.export', 'symmetry-representation>=0.2', 'click', 'bands-inspect',
        'fsc.hdf5-io>=0.2.0'
    ],
    extras_require=EXTRAS_REQUIRE,
    long_description=README,
    classifiers=[  # yapf:disable
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Physics'
    ],
    entry_points='''
        [console_scripts]
        tbmodels=tbmodels._cli:cli
    ''',
    license='Apache 2.0',
    packages=['tbmodels', 'tbmodels._ptools']
)
