# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['luffa']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'luffa',
    'version': '0.0.0',
    'description': 'Luffa.io command line client',
    'long_description': None,
    'author': 'Hadrien David',
    'author_email': 'hadrien@ectobal.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
