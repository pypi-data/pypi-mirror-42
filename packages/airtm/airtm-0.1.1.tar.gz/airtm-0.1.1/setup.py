# -*- coding: utf-8 -*-
from setuptools import setup
setup(
  name = 'airtm',
  packages = ['airtm'],
  version = '0.1.1',
  description = "Library for AirTM's API",
  long_description="A python library for interfacing with the AirTM API.",
  author = 'AirTM',
  author_email = 'partners@airtm.io',
  url = 'https://bitbucket.org/airtm/payments-sdk-python',
  download_url = '',
  keywords = ['airtm', 'api'],
  classifiers = [],
  install_requires=[
        'urllib3','requests','configparser','pprint'
  ],
)
