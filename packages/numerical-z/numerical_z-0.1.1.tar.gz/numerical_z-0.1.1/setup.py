#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

requirements = ["numpy", "numba", "scipy", "plasmapy",  ]

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
    description="Compute the plasma equation Z from any EVDF",
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description='\n\n',
    include_package_data=True,
    keywords='numerical_z',
    name='numerical_z',
    packages=find_packages(include=['numerical_z']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://hephaistos.lpp.polytechnique.fr/rhodecode/GIT_REPOSITORIES/LPP/Users/Tavant/DevCalcul/Numerical_Z',
    version='0.1.1',
    zip_safe=False,
)
