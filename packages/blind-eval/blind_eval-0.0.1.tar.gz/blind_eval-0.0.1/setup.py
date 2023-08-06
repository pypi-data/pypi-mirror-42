#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='blind_eval',
    version='0.0.1',
    author='wanglbox',
    author_email='wanglbox@gmail.com',
    url='https://www.linkedin.com/in/leo-wang-amzn/',
    description=u'model evaluation',
    packages=['blind_eval'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'benchmark=blind_eval:benchmark',
            'plot=blind_eval:plot'
            'evaluate_set=blind_eval:evaluate_set'
        ]
    }
)
