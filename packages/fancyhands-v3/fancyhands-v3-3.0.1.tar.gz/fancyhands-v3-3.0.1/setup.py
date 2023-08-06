#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='fancyhands-v3',
    version='3.0.1',

    description='fancyhands.com python API',
    url='https://github.com/fancyhands/fancyhands-python-v3',

    author='Fancy Hands',
    author_email='api@fancyhands.com',

    packages = find_packages(),
    license='MIT',

    install_requires = ['httplib2', 'oauth2',],
    include_package_data = True,
)
