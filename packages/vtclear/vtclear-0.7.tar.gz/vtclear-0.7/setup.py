#!/usr/bin/env python3

import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vtclear",
    packages=["vtclear"],
    version="0.7",
    license="GPL3",
    description="Python3 ANSI VT100 implementation of Erase Screen.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Carlos A. Planchón",
    author_email="bubbledoloresuruguay2@gmail.com",
    url="https://github.com/carlosplanchon/vtclear",
    download_url="https://github.com/carlosplanchon/"
        "vtclear/archive/v0.7.tar.gz",
    keywords=["CLEAR", "VT100", "ANSI"],
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
