#!/usr/bin/env python3
import os, json
from setuptools import setup, find_packages

PROJ_NAME = 'rwords'
PACKAGE_NAME = 'rwords'
VERSION = '0.0.0.rc.102'
PROJ_METADATA = '{}.json'.format(PACKAGE_NAME)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

with open("README.md", "r") as fh:
    README = fh.read()


setup(
    name=PROJ_NAME,
    version=VERSION,
    description='Rwords',
    long_description='A command line tool to help you remember words faster.',
    author='endlex',
    author_email="endlex@aliyun.com",
    license='MIT',
    packages=find_packages(),
    data_files=[('', ['LICENSE', ]), ],
    python_requires='>=3.4,',
    py_modules=['rwords'],
    install_requires=['docopt', 'requests>2.0', 'sqlalchemy>=1.2', 'readchar', 'pygame>=1.6'],

    entry_points={
        'console_scripts': [
            'rw=rwords.rw:main',
        ],
    },
)
