#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Sun Wei"
__copyright__ = "Copyright (C) 2019 GFLoan Co. LTD"
__license__ = "Private"
__version__ = "1.0"

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-pkg-wei",
    version="1.0.2",
    author="Example Author",
    author_email="sw@gfloan.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=['bin/hello-joke'],
    entry_points={
        'console_scripts': ['entry_joke=example_pkg_wei.command_line:main']
    }
)
