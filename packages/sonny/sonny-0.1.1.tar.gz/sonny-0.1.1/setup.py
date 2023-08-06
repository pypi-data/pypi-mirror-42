#!/usr/bin/env python3

from codecs import open
from sonny import __version__
from setuptools import setup


def read(f):
    return open(f, encoding='utf-8').read()


setup(
    name='sonny',
    version=__version__,
    description='A command line translation software.',
    long_description=read('README.rst') + '\n\n' + read('HISTORY.rst'),
    author='suowei',
    author_email='suowei_66@qq.com',
    url='',
    packages=[
        'sonny'
    ],
    py_modules=['run'],
    include_package_data=True,
    platforms='any',
    install_requires=[
    ],
    entry_points={
        'console_scripts': ['sonny=run:cli']
    },
    license='MIT',
    zip_safe=False,
    classifiers=[
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython'
    ]
)
