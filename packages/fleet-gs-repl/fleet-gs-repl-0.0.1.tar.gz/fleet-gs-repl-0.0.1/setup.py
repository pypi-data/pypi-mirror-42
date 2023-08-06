#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import inspect
import os
import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

install_requires = [
    "click",
    "aioconsole",
    "blessings",
    "hbmqtt",
    "yarl",
]


def readme():
    try:
        return open('README.md', encoding='utf-8').read()
    except TypeError:
        return open('README.md').read()

setup(
    name='fleet-gs-repl',
    packages=find_packages(),
    version='0.0.1',
    description='internal tool for sending messages on mqtt',
    long_description=readme(),
    author='Fleet Space Technologies',
    url='https://bitbucket.org/fleetspace/gs_repl/src',
    install_requires=install_requires,
    entry_points={'console_scripts': ['gs = gs.cli:main']}
)
