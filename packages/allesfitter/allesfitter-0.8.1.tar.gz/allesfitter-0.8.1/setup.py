#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 11:40:38 2019

@author:
Maximilian N. Günther
MIT Kavli Institute for Astrophysics and Space Research, 
Massachusetts Institute of Technology,
77 Massachusetts Avenue,
Cambridge, MA 02109, 
USA
Email: maxgue@mit.edu
Web: www.mnguenther.com
"""

from setuptools import setup, find_packages

setup(
    name = 'allesfitter',
    packages=find_packages(),
    version = '0.8.1',
    description = 'A global inference framework for photometry and RV',
    author = 'Maximilian N. Günther & Tansu Daylan',
    author_email = 'maxgue@mit.edu',
    url = 'https://github.com/MNGuenther/allesfitter',
    download_url = 'https://github.com/MNGuenther/allesfitter',
    classifiers = []
    #install_requires=['numpy>=1.10'],
    #include_package_data = True
    )



