#!/usr/bin/env python3

from setuptools import setup
import os
import sys

sys.path.insert(0, '.')
import hashget

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='hashget',
    version=hashget.version,
    packages=['hashget'],
    scripts=['bin/hashget', 'bin/hashget-admin'],

    install_requires=['patool','filetype','filelock'],

    url='https://gitlab.com/yaroslaff/hashget',
    license='MIT',
    author='Yaroslav Polyakov',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author_email='yaroslaff@gmail.com',
    description='hashget deduplication and compression tool'
)
