#!/usr/bin/env python

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='scotusutils',
    version='0.1dev',
    description='SCOTUS Analysis Tools',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Thomas Richardson II',
    author_email='immersinn@gmail.com',
    packages=['scotusutils'],
    scripts=['bin/scotus-data-init'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    url="https://github.com/pypa/sampleproject",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
