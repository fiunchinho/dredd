#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Jose Armesto
"""
from codecs import open
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dredd',
    version='1.0.0',
    author='Jose Armesto',
    author_email='jose@armesto.net',
    packages=find_packages('.'),
    include_package_data=True,
    url='https://github.com/fiunchinho/dredd',
    description='Terminate healthy instances containing unhealthy services',
    long_description=long_description,
    license='GPLv2',
    install_requires=open('requirements.txt').read().split(),
    entry_points={
        "console_scripts": ["dredd = dredd.cli:main"]
    },
    classifiers=[],
    keywords='eureka consul aws'
)
