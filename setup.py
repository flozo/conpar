#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Setup module for conpar."""


from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Use README.md file as long description
long_description = (here/'README.md').read_text(encoding='utf-8')

setup(
        name='conpar',
        version='0.11',
        description='A parser for configuration files.',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/flozo/conpar',
        author='flozo',
        author_email='github.mail@flozo.de',
        # Classifiers from https://pypi.org/classifiers/
        classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'Environment :: Console',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: GNU General Public License v3'
            ' or later (GPLv3+)',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            ],
        keywords='configuration, parser, conversion, plain text, '
        'human readable, JSON, INI',
        package_dir={'': 'src'},
        packages=find_packages(where='src'),
        install_requires=['argparse', 'pandas', 'os', 'json', 'colorama'],
    )
