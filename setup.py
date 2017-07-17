#!/usr/bin/env python3

from setuptools import setup

with open('README.md', 'r') as f:
    description = f.read()

setup(
    name = 'py-oeis',
    version = '1.1',
    description = description,
    author = 'Sumant Bhaskaruni',
    author_email = 'bsumantb@gmail.com',
    license = 'MIT',
    url = 'https://github.com/totallyhuman/py-oeis',
    py_modules = ['oeis'],
    install_requires = ['pendulum', 'requests']
)
