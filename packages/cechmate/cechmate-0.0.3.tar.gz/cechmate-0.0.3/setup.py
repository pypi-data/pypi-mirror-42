#!/usr/bin/env python

from setuptools import setup


import re
VERSIONFILE="cechmate/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

with open('README.md') as f:
    long_description = f.read()

setup(name='cechmate',
      version=verstr,
      description='Custom filtration builders.',
      long_description=long_description,
      long_description_content_type="text/markdown",	
      author='Christopher Tralie, Nathaniel Saul',
      author_email='chris.tralie@gmail.com, nat@saulgill.com',
      url='https://github.com/scikit-tda/cechmate',
      license='MIT',
      packages=['cechmate'],
      include_package_data=True,
      install_requires=[
        'scipy',
        'numpy',
        'matplotlib',
        'phat'
      ],
      extras_require={ # use `pip install -e ".[testing]"``
        'testing': [
          'pytest' 
        ],
        'docs': [ # `pip install -e ".[docs]"``
          'sphinx',
          'nbsphinx',
          'sphinx-better-theme',
          'sphinxcontrib-fulltoc'
        ]
      },
      python_requires='>=2.7,!=3.1,!=3.2,!=3.3',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Healthcare Industry',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
      ],
      keywords='persistent homology, persistence images, persistence diagrams, topology data analysis, algebraic topology, unsupervised learning'
     )
