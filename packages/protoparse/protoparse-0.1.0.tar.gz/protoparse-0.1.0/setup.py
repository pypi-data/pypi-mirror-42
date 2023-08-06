# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['protoparse']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'protoparse',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Thibaut Le Page',
    'author_email': 'thibaut.le.page@zalando.de',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
