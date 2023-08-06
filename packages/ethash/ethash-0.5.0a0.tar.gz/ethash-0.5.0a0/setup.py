#!/usr/bin/env python3

from setuptools import setup

setup(
    name='ethash',
    version='0.5.0-alpha.0',
    url='https://github.com/chfast/ethash',
    author='Paweł Bylica',
    author_email='pawel@ethereum.org',

    package_dir={'': 'bindings/python'},
    packages=['ethash'],
    cffi_modules=['bindings/python/ethash_build.py:ffibuilder'],

    setup_requires=['cffi>=1.12'],
    install_requires=['cffi>=1.12'],
)
