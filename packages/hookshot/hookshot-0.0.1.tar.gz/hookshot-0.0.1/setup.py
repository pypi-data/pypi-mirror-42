#!/usr/bin/env python

import hookshot
from setuptools import setup

setup(
    name='hookshot',
    packages=['hookshot'],
    version=hookshot.__version__,
    description='hookshot',
    license='MIT',
    url='https://github.com/vesche/hookshot',
    author=hookshot.__author__,
    author_email=hookshot.__email__,
    entry_points={
        'console_scripts': [
            'hookshot = hookshot.hookshot:main',
        ]
    },
    install_requires=[],
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ]
)
