#!/usr/bin/env python

import setuptools

MAJOR       = 0
MINOR       = 11
PRERELEASE  = 'alpha'
ISRELEASED  = False
if PRERELEASE:
  VERSION = '%d.%d-%s' % (MAJOR, MINOR, PRERELEASE)
else:
  VERSION = '%d.%d' % (MAJOR, MINOR)

with open("README.md", "r") as fp:
  long_description = fp.read()

setuptools.setup(
  name='VenomSeq',
  version=VERSION,
  description='Python code for performing the data analysis in the VenomSeq workflow',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author='Joseph D. Romano',
  author_email='jdromano2@gmail.com',
  url='https://github.com/jdromano2/venomseq',
  packages=['venomseq'],
  package_dir={'venomseq': 'venomseq'},
  classifiers=[
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Programming Language :: Python :: 3.6",
    "Topic :: Scientific/Engineering :: Bio-Informatics"
  ],
  install_requires=[
    'numpy',
    'scipy',
    'pandas',
    'matplotlib',
    'tqdm'
  ]
)