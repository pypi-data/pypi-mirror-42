#!/usr/bin/env python

from setuptools import (
    setup as install,
    find_packages,
)

VERSION = '0.0.5.4'

install(
    name='ppt',
    version=VERSION,
    description="The Python Performance Tuner",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Seb Arnold',
    author_email='smr.arnold@gmail.com',
    url='http://www.seba1511.com',
    download_url='https://github.com/seba-1511/ppt/archive/' + str(VERSION) + '.zip',
    license='License :: OSI Approved :: Apache Software License',
    packages=find_packages(exclude=["tests"]),
    classifiers=[],
    install_requires=[
       'numpy',
       'visdom>=0.1.7.2',
    ],
)
