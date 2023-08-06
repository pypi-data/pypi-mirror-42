#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from codecs import open

with open('README.rst', encoding='utf-8') as f:
    readme = f.read()

with open('requirements.txt', encoding='utf-8') as f:
    requirements = f.read().splitlines()

with open('requirements_dev.txt', encoding='utf-8') as f:
    test_requirements = f.read().splitlines()


setup(
    name='hjoin',
    version='0.2.0',
    description="Horizontal join",
    long_description=readme,
    author="Jonathan Eunice",
    author_email='jonathan.eunice@gmail.com',
    url='https://github.com/jonathaneunice/hjoin',
    packages=[
        'hjoin',
    ],
    install_requires=requirements,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='hjoin',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    test_suite='test',
    tests_require=test_requirements
)
