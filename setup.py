#!/usr/bin/env python

from setuptools import setup

setup(name='tabletext',
      version='0.1',
      description='Python library and command line utility to pretty-print\
      tabular data',
      long_description=open("README.rst").read() + "\n"
      + open("CHANGELOG.rst").read(),
      url='https://github.com/Thibauth/tabletext',
      author='Thibaut Horel',
      author_email='thibaut.horel+tabletext@gmail.com',
      py_modules=['tabletext'],
      entry_points={"console_scripts": ["table=tabletext:main"]},
      use_2to3=True,
      license='GNU GPLv3'
      )
