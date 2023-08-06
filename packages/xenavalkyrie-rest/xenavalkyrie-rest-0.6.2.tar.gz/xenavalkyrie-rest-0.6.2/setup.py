#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function
from setuptools import setup, find_packages
import io

import xenavalkyrie_rest


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


with open('requirements.txt') as f:
    required = f.read().splitlines()
install_requires = [r for r in required if r and r[0] != '#' and not r.startswith('git')]

long_description = read('README.rst')

setup(
    name='xenavalkyrie-rest',
    version=xenavalkyrie_rest.__version__,
    url='https://github.com/xenadevel/RestXenaValkyrie/',
    license='Apache Software License',
    author='Yoram Shamir',
    install_requires=install_requires,
    author_email='yoram@ignissoft.com',
    description='Stand-alone REST API server to manage Xena Valkyrie chassis',
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    tests_require=['pytest'],
    py_modules=['xena_rest_server'],
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Testing :: Traffic Generation',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6'],
)
