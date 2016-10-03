#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pip.req import parse_requirements

import datetimemocker

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = datetimemocker.__version__

readme = open('README.rst').read()

requirements = [str(req.req) for req in parse_requirements('requirements.txt', session=False)]

setup(
    name='datetimemocker',
    version=version,
    description="""Mock the datetime and date classes in all loaded python files.""",
    long_description=readme,
    author='Toby Nance',
    author_email='toby.nance@draft2digital.com',
    url='https://github.com/Draft2Digital/d2datetimemocker',
    packages=[
        'datetimemocker',
    ],
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='datetime date timezone django mock mock-datetime testing mocking',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
)
