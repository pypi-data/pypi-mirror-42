#!/usr/bin/env python
from __future__ import absolute_import, print_function

import io

from setuptools import setup, find_packages


def _read(filename, as_lines=True):
    with io.open(filename, encoding='utf-8') as handle:
        if as_lines:
            return [line.strip('\n').strip() for line in handle.readlines()]
        return handle.read()


setup(
    name='django-minimal-user',
    version='0.9.2',
    description='Bare minimum user model for Django',
    long_description=_read('README.md', as_lines=False),
    author='Ionata Digital',
    author_email='webmaster@ionata.com.au',
    url='https://github.com/ionata/django-minimal-user',
    packages=find_packages(),
    include_package_data=True,
    install_requires=_read('requirements-production.txt'),
    extras_require={'drf': _read('requirements-extras-drf.txt')},
    python_requires='>=3.5',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
