# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['tote']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tote',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jared Lunde',
    'author_email': 'jared.lunde@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
