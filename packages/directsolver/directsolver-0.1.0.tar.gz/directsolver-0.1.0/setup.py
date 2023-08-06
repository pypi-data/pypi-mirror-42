#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

requirements = [ ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Antoine Tavant",
    author_email='antoinetavant@hotmail.fr',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Minimise a function in the complex plan",
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description= '\n\n' ,
    include_package_data=True,
    keywords='directsolver',
    name='directsolver',
    packages=find_packages(include=['directsolver']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/antoinelpp/directsolver',
    version='0.1.0',
    zip_safe=False,
)
