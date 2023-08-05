#!/usr/bin/env python

from distutils.core import setup
from setuptools import *
import os

setup(
    name="torclient",
    version="1.0.6",
    description="A Simple, Lightweight and Easy To Use, TOR Proxy Library For Python",
    author="noctua",
    author_email="psmall.775@gmail.com",
    url="https://github.com/noctua-github",
    packages=["torclient"],
    classifiers=[
              "Programming Language :: Python",
 #             "Intended Audience :: Penetration Testers/Developers",
#              "Topic :: Networking"
    ],
    install_requires=[
              'setuptools',
              'stem',
              'requests',
              'pysocks'
    ]
)
