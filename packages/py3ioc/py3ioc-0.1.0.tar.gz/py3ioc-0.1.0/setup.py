# coding=utf-8
import os
from setuptools import setup

PATCH_VERSION = os.getenv('PYIOC_PATCH_VERSION', '0')
setup(
    name='py3ioc',
    version='0.1.%s' % PATCH_VERSION,
    packages=['pyioc'],
    url='https://github.com/artsalliancemedia/pyioc',
    license='MIT',
    author='',
    author_email='',
    description='Python3 IoC tools.',
    install_requires=[
    ],
    extras_require={
        'test': [
            'pytest>=2.8.0',
            'mock>=1.3.0',
            'coverage>=4.0.0'
        ],
        'dev': [
            'ipython',
            'flake8'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)
