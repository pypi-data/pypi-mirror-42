# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os.path
from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name = "epigeec_ihecmetadata",
    version = "0.1.0",
    author = "Simon Hébert-Deschamps",
    author_email = "simon.hebert-deschamps@usherbrooke.ca",
    description = "A convenient and generic way of using IHEC DataPortal JSON",
    packages = find_packages(exclude=['test']),
    install_requires = [
    ],
    python_requires='>=2.7.5, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',
    license = "ECL",
    long_description = LONG_DESCRIPTION,
    long_description_content_type = 'text/markdown',
    url = 'https://gitlab.com/labjacquespe/epigeec_ihecmetadata/tree/master',
    classifiers = [
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Intended Audience :: Science/Research',
        'Environment :: Console',
    ],
)