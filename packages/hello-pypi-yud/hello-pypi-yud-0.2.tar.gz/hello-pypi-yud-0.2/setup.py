#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='hello-pypi-yud',
    version=0.2,
    description=(
        '这是一个测试'
    ),
    long_description='这是一个测试',
    author='yud',
    author_email='dengyu326@gmail.com',
    maintainer='yud',
    maintainer_email='dengyu326@gmail.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)
