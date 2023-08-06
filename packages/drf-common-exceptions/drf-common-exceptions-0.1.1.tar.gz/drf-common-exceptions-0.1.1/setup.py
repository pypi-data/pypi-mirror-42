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
    'version': '0.1.1',
    'description': 'Common exception for Django REST framework',
    'long_description': 'drf-common-exceptions\n===\n\n| Release | CI | Coverage |\n|---------|----|----------|\n|[![pypi](https://img.shields.io/pypi/v/drf-common-exceptions.svg)](https://pypi.python.org/pypi/drf-common-exceptions)|[![build](https://img.shields.io/travis/com/abogoyavlensky/drf-common-exceptions.svg)](https://travis-ci.com/abogoyavlensky/drf-common-exceptions)|[![codecov](https://img.shields.io/codecov/c/github/abogoyavlensky/drf-common-exceptions.svg)](https://codecov.io/gh/abogoyavlensky/drf-common-exceptions)|\n\nCommon exception for Django REST framework. Provides single generic interface of\nreturning data structure for any kind of exceptions which are handled by\nDjango REST framework. Includes error name, path to service with line\nwhere the error occurs and a list of actual error messages\nwith extended fields info.\n\n## Requirements\n\n- Python (3.6+)\n- Django (1.11.x, 2.0+)\n- Django REST Framework (3.7+)\n\n## Installation\n\n```bash\n$ pip install drf-common-exceptions\n```\n\n## Usage examples\n\nYou can define common exception handler for whole project. Just put the\nfollowing line to your django settings inside drf section:\n\n```\nREST_FRAMEWORK = {\n  ...\n  "EXCEPTION_HANDLER": "drf_common_exceptions.common_exception_handler",\n  ...\n}\n```\n\nOr use it just for particular view or viewset:\n\n```python\nfrom drf_common_exceptions import CommonExceptionHandlerMixin\n\nclass MyView(CommonExceptionHandlerMixin, APIView):\n    pass\n```\n\nThe output will looks like for example validation error:\n```json\n{\n    "service": "path.to.views.MyView:20",\n    "error": "ValidationError",\n    "detail": [\n        {\n            "label": "Name",\n            "field": "name",\n            "messages": [\n                "This is required field."\n            ]\n        }\n    ]\n}\n```\n\nThe data structure will be the same for any other errors.\n\n## Development\n\nInstall poetry and requirements:\n\n```bash\n$ curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python\n$ python3 -m venv path/to/venv\n$ source path/to/venv/bin/activate\n$ poetry install\n```\n\nRun main commands:\n\n```bash\n$ make test\n$ make watch\n$ make clean\n$ make lint\n```\n\nPublish to pypi be default patch version:\n```bash\n$ make publish\n```\n\nor any level you want:\n```bash\n$ make publish minor\n```\n',
    'author': 'Andrey Bogoyavlensky',
    'author_email': 'abogoyavlensky@gmail.com',
    'url': 'https://github.com/abogoyavlensky/drf-common-exceptions',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
