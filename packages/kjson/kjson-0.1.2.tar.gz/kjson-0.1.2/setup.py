#!/usr/bin/env python

import os.path

from setuptools import setup, find_packages


dirname = os.path.dirname(os.path.abspath(__file__))


setup(
    name="kjson",
    version="0.1.2",
    description="A JSON encoder and decoder with support for Python types.",
    long_description=open(os.path.join(dirname, 'README.md')).read(),
    url="https://bitbucket.org/tran-smit/py-kjson",
    author_email="frank@tran-smit.nl",
    author="Tran-Smit Software",
    license="ISC",
    python_requires=">=3.6.0",
    packages=find_packages(),
    install_requires=(
        "ciso8601",
    ),
    tests_require=(
        "django",
        "parameterized",
        "pytz",
    )
)
