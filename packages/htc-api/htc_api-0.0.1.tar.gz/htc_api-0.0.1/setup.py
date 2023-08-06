#!/usr/bin/env python

import htc_api
from setuptools import setup

setup(
    name='htc_api',
    packages=['htc_api'],
    version=htc_api.__version__,
    description='Hack The Classroom API',
    license='MIT',
    url='https://github.com/hacktheclassroom/htc-api',
    author='Spencer Hanson and Austin Jackson',
    author_email='hacktheclassrooms@gmail.com',
    install_requires=['requests'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Topic :: Security"
    ]
)