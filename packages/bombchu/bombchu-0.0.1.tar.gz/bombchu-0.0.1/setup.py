#!/usr/bin/env python

import bombchu
from setuptools import setup

setup(
    name='bombchu',
    packages=['bombchu'],
    version=bombchu.__version__,
    description='bombchu',
    license='MIT',
    url='https://github.com/vesche/bombchu',
    author=bombchu.__author__,
    author_email=bombchu.__email__,
    entry_points={
        'console_scripts': [
            'bombchu = bombchu.bombchu:main',
        ]
    },
    install_requires=[],
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ]
)
