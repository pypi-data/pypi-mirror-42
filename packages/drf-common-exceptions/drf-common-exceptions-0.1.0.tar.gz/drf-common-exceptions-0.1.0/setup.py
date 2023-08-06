# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['drf_common_exceptions']

package_data = \
{'': ['*']}

install_requires = \
['django>=1.11', 'djangorestframework>=3.7,<4.0']

setup_kwargs = {
    'name': 'drf-common-exceptions',
    'version': '0.1.0',
    'description': 'Common exception for Django REST framework',
    'long_description': None,
    'author': 'Andrey Bogoyavlensky',
    'author_email': 'abogoyavlensky@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
