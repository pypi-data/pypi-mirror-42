#!/usr/bin/python
import io
import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, 'README.rst'), encoding='utf8') as f:
        README = f.read()

setup(
    name='http_ece',
    version='1.1.0',
    author='Martin Thomson',
    author_email='martin.thomson@gmail.com',
    scripts=[],
    packages=['http_ece'],
    description='Encrypted Content Encoding for HTTP',
    long_description='Encipher HTTP Messages',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='crypto http',
    install_requires=[
        'cryptography>=2.5',
    ],
    tests_require=[
        'nose',
        'mock',
        'coverage',
        'flake8',
    ],
    test_suite="nose.collector",
    url='https://github.com/martinthomson/encrypted-content-encoding',
    license='MIT'
)
