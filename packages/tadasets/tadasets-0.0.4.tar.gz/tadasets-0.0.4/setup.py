#!/usr/bin/env python

from setuptools import setup


import re
VERSIONFILE="tadasets/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))


with open('README.md') as f:
    long_description = f.read()

setup(name='tadasets',
      version=verstr,
      description='Great data sets for Topological Data Analysis.',
      long_description=long_description,
      long_description_content_type="text/markdown",	
      author='Nathaniel Saul',
      author_email='nathaniel.saul@wsu.edu',
      url='https://tadasets.scikit-tda.org',
      license='MIT',
      packages=['tadasets'],
      include_package_data=True,
      extras_require={ #use `pip install -e ".[testing]"``
        'testing': [
          'pytest',
          'scipy'   
        ],
        'docs': [ # `pip install -e ".[docs]"``
          'sphinx',
          'nbsphinx',
          'sphinx-better-theme',
          'sphinxcontrib-fulltoc'
        ]
      },
      install_requires=[
        'numpy',
        'matplotlib',
      ],
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
      keywords='topological data analysis, data sets, test data'
     )
