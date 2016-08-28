#!/usr/bin/python

import os
import sys

from setuptools import find_packages, setup

from broadcast import __version__


SCRIPTDIR = os.path.dirname(__file__) or '.'
PY3 = sys.version_info >= (3, 0, 0)


def read(fname):
    """ Return content of specified file """
    path = os.path.join(SCRIPTDIR, fname)
    if PY3:
        f = open(path, 'r', encoding='utf8')
    else:
        f = open(path, 'r')
    content = f.read()
    f.close()
    return content


setup(
    name='broadcast-portal',
    version=__version__,
    author='Outernet Inc',
    author_email='apps@outernet.is',
    description='Portal for submitting content to Outernet',
    license='GPLv3',
    keywords='broadcast, outernet, content, zip, json',
    url='https://github.com/Outernet-Project/broadcast-portal',
    packages=find_packages(),
    long_description=read('README.rst'),
    install_requires=read('requirements.txt').strip().split('\n'),
    entry_points={
        'console_scripts': [
            'broadcast = broadcast.main:main',
        ]
    },
)
