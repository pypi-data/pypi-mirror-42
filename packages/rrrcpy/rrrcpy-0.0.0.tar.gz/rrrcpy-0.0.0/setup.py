#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function


import os
from setuptools import find_packages, setup


about = {
    "__title__": "rrrcpy",
    "__version__": "0.0.0",
    "__summary__": "",
    "__email__": "",
    "__author__": "",
}


setup_requirements = [
]
test_requirements = [
]

long_description = ""


setup(
    name=about["__title__"],
    version=about["__version__"],

    description=about["__summary__"],
    long_description=long_description,
    long_description_content_type="text/markdown",

    author=about["__author__"],
    author_email=about["__email__"],

    classifiers=[
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
    ],

    packages=find_packages(exclude=['tests', 'test_*', "tests.*"]),
    include_package_data=True,

    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',

    install_requires=[
    ] + setup_requirements,
    tests_require=test_requirements,
    extras_require={
        "test": test_requirements,
        "docs": [
        ],
        "docstest": [
        ],
        "pep8test": [
        ],
    },
)