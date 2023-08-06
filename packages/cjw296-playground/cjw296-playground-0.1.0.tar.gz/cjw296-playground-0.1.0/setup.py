# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['playground']
install_requires = \
['pkginfo>=1.4,<2.0', 'requests>=2.21,<3.0', 'sphinx>=1.8,<2.0']

setup_kwargs = {
    'name': 'cjw296-playground',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Chris Withers',
    'author_email': 'chris@withers.org',
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
