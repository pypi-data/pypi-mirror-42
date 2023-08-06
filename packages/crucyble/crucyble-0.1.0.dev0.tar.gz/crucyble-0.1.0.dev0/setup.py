# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['crucyble']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'crucyble',
    'version': '0.1.0.dev0',
    'description': 'A Cython Wrapped GloVe',
    'long_description': None,
    'author': 'Tyler Kontra',
    'author_email': 'tyler@tylerkontra.com',
    'url': 'https://github.com/ttymck/crucyble',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
