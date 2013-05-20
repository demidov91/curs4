#!/usr/bin/env python
 
from setuptools import setup, find_packages
 

 
setup(
  name="curs",
  version="1.0",
  description="Recommendation system",
  author="demidov",
  packages = find_packages('curs'),
  package_dir = {'': 'curs'},
  include_package_data = True,
  zip_safe = False,
  install_requires=[
    'django == 1.5.1',
    'neomodel',
    'psycopg2',
    'south',
    'openpyxl',
  ]
)
