#!/usr/bin/env python

import mirrorshield
from setuptools import setup

setup(
    name='mirrorshield',
    packages=['mirrorshield'],
    version=mirrorshield.__version__,
    description='mirrorshield',
    license='MIT',
    url='https://github.com/vesche/mirrorshield',
    author=mirrorshield.__author__,
    author_email=mirrorshield.__email__,
    entry_points={
        'console_scripts': [
            'mirrorshield = mirrorshield.mirrorshield:main',
        ]
    },
    install_requires=[],
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ]
)
