#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pip

from pip.req import parse_requirements

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

parsed_requirements = parse_requirements(
    'requirements/prod.txt',
    session=pip.download.PipSession()
)

parsed_test_requirements = parse_requirements(
    'requirements/tests.txt',
    session=pip.download.PipSession()
)


requirements = [str(ir.req) for ir in parsed_requirements]
test_requirements = [str(tr.req) for tr in parsed_test_requirements]


setup(
    name='switchy-witchy',
    version='0.1.0',
    description="A simple tcp message util for capturing sys info.",
    long_description=readme + '\n\n' + history,
    author="Maxwell J. Resnick",
    author_email='max@ofmax.li',
    url='https://gitlab.com/grumps/switchy-witchy',
    packages=[
        'switchy-witchy',
    ],
    package_dir={'switchy-witchy':
                 'switchy-witchy'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='switchy-witchy',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests.run_tests',
    tests_require=test_requirements
)
