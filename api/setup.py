#!/usr/bin/env python3

from setuptools import find_packages, setup

setup(
    name='api',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask-cli==0.4.0',
        'flask-cors==3.0.10',
        'pymongo==4.0.1',
        'pyjwt==1.7.1',
    ],
)
