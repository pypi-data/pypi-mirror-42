#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(C) Copyright 2018-2019 Hewlett Packard Enterprise Development LP

StoreOnce REST client SDK
"""

import os
import io
from setuptools import setup, find_packages  # noqa: H301

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

NAME = "storeonce-client"
VERSION = "1.4.1.1.8"
DESCRIPTION = "A StoreOnce REST client SDK"
AUTHOR = "Hewlett Packard Enterprise Development LP"
LICENSE = "MIT"
REQUIRES_PYTHON = ">=2.7.0, !=3.0, !=3.1, !=3.2, !=3.3, <4"

# Use README as long description if available
here = os.path.abspath(os.path.dirname(__file__))
try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

REQUIRES = ["urllib3>=1.15", "six>=1.10", "certifi", "python-dateutil"]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    keywords=["Swagger", "StoreOnce", "REST", "SDK"],
    packages=find_packages(),
    python_requires=REQUIRES_PYTHON,
    install_requires=REQUIRES,
    include_package_data=True,
    license=LICENSE,
    classifiers={
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython"
    },
)
