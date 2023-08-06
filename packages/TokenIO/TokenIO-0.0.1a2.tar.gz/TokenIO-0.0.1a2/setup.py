# -*- coding: utf-8 -*-

import tokenio
from os import path

from setuptools import setup, find_packages

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

install_requires = open("requirements.txt").readlines()

setup(
    name='TokenIO',
    version=tokenio.__version__,
    author='overcat',
    author_email='4catcode@gmail.com',
    url='https://github.com/overcat/token-io',
    packages=find_packages(),
    keywords=['token', 'token_io'],
    description='Python SDK for interacting with the Token System',
    long_description=long_description,
    long_description_content_type='text/markdown',
    platforms='any',
    python_requires='>=3.5',
    install_requires=install_requires,
    include_package_data=True,
    license='MIT License',
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
