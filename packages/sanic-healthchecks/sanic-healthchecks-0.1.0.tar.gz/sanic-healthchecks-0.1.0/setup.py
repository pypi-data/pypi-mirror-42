# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['sanic_healthchecks']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.5,<4.0']

setup_kwargs = {
    'name': 'sanic-healthchecks',
    'version': '0.1.0',
    'description': 'A small wrapper for making it easy to add a healthcheck server to your Sanic application',
    'long_description': '',
    'author': 'Aaron',
    'author_email': 'AaronBatilo@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
