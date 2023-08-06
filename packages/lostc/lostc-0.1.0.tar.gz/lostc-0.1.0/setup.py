#!/usr/bin/env python

"""
suanpan
"""
import os

from setuptools import find_packages, setup


def read_file(path):
    with open(path, "r") as f:
        return f.read()


README = "README.md"
packages = find_packages()

setup(
    name="lostc",
    version="0.1.0",
    packages=packages,
    license="See License",
    author="majik",
    author_email="me@yamajik.com",
    description=read_file(README),
    long_description=__doc__,
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
