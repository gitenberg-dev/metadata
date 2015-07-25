#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]


setup(
    name='gitenberg.metadata',
    version='0.1.0',
    description="metadata development - formats and machinery for GITenberg",
    long_description=readme + '\n\n' + history,
    author="Raymond Yee",
    author_email='raymond.yee@gmail.com',
    url='https://github.com/gitenberg-dev/metadata',

    namespace_packages=['gitenberg'],
    packages=find_packages(exclude=[]),
    include_package_data=True,
    install_requires=requirements,
    license="GPL",
    zip_safe=False,
    keywords='gitenberg.metadata',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
