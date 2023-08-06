# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['fast_rpc', 'fast_rpc.protocol', 'fast_rpc.serialization']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fast-rpc',
    'version': '0.1.0',
    'description': 'Pure python implementation of binary FastRPC format de/serialisation',
    'long_description': None,
    'author': 'Ken Mijime',
    'author_email': 'kenaco666@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
