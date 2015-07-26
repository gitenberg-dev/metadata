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
    "pymarc==3.0.3",
    "PyYAML==3.11",
    "six==1.9.0",
    "SPARQLWrapper==1.6.4",
    "html5lib==0.999999",
    "isodate==0.5.1",
    "pyparsing==2.0.3",
    "rdflib==4.2.0",
    "rdflib-jsonld==0.3",
]

test_requirements = [
    "nose==1.3.7"
]


setup(
    name='gitenberg.metadata',
    version='0.1.6',
    description="metadata development - formats and machinery for GITenberg",
    long_description=readme + '\n\n' + history,
    author="Eric Hellman",
    author_email='eric@hellman.net',
    url='https://github.com/gitenberg-dev/metadata',

    namespace_packages=['gitenberg'],
    packages=find_packages(exclude=[]),
    include_package_data=True,
    install_requires=requirements,
    license="GPL",
    zip_safe=False,
    keywords="books ebooks gitenberg gutenberg epub metadata",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.3',
        # 'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
