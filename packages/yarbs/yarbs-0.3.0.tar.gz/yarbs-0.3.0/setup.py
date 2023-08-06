#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A setuptools based setup module.
"""

# Version number is fetched directly from the package.
# The same can be done with __author__ if you want. For more info see:
# https://www.python.org/dev/peps/pep-0008/#module-level-dunder-names
from yarbs import __version__

from setuptools import setup, find_packages

# Name of the packaged distribution.
# If you're packaging a single Python package it is typically the same name.
distributionName = 'yarbs'

setup(
    #
    # Basic options.
    #

    name=distributionName,

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=__version__,

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=[
        'yarbs',
        ],

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this (can be combined with "packages"):
    #py_modules=[],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        ],

    #
    # Extra options.
    #

    cmdclass={
        },

    # If there are data files included in your packages that need to be
    # installed, specify them here.
    package_data={
        # You can for example include test data:
        # 'yarbs': [ 'TestData/*.dat' ],

        # Or you can use this to include a C/C++ extension and libraries:
        # 'yarbs': [
        #    '*.pyd',
        #    '*.dll',
        #    '*.so',
        #    # Matches any versioned libraries on Linux-like environment
        #    # (e.g. "libboost.so.1.55").
        #    'lib*',
        #    ]
        },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    data_files=[
        ],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        },

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        },

    #
    # Informational options.
    # These are optional.
    #

    # The project's main homepage.
    # If you're using some GitLab or similar (you should), provide the project link.
    url='https://gitlab.com/maranov/yarbs',

    # Author details.
    author='maranov',
    author_email='maranov@outlook.com',

    # Choose your license.
    license='WTFPL',

    # What does your project relate to?
    keywords='rsync backup',

    # Short description.
    description='Create incremental backups using Rsync.',

    # Long description can be loaded from Readme file or you can just
    # write it down.
    long_description=open('Readme.md').read(),

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
       # How mature is this project? Common values are
       #   3 - Alpha
       #   4 - Beta
       #   5 - Production/Stable
       'Development Status :: 4 - Beta',

       # Indicate who your project is intended for
       'Intended Audience :: System Administrators',
       'Topic :: System :: Archiving :: Backup',

       # Pick your license as you wish (should match "license" above)
    #   'License :: WTFPL',
    #
    #    # Specify the Python versions you support here. In particular, ensure
    #    # that you indicate whether you support Python 2, Python 3 or both.
    #    'Programming Language :: Python :: 2',
    #    'Programming Language :: Python :: 2.7',
    #    'Programming Language :: Python :: 3',
    #    'Programming Language :: Python :: 3.3',
    #    'Programming Language :: Python :: 3.4',
    #    'Programming Language :: Python :: 3.5',
    #    'Programming Language :: Python :: 3.6',
       'Programming Language :: Python :: 3.7',
       ],
    )
