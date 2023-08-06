#!/usr/bin/env python

import hoverboots
from setuptools import setup

setup(
    name='hoverboots',
    packages=['hoverboots'],
    version=hoverboots.__version__,
    description='hoverboots',
    license='MIT',
    url='https://github.com/vesche/hoverboots',
    author=hoverboots.__author__,
    author_email=hoverboots.__email__,
    entry_points={
        'console_scripts': [
            'hoverboots = hoverboots.hoverboots:main',
        ]
    },
    install_requires=[],
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ]
)
