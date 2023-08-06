# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['cafeteria',
 'cafeteria.abc',
 'cafeteria.datastructs',
 'cafeteria.datastructs.units',
 'cafeteria.decorators',
 'cafeteria.logging',
 'cafeteria.patterns',
 'cafeteria.patterns.context',
 'cafeteria.twisted']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=3.13,<4.0', 'six>=1.12,<2.0']

extras_require = \
{':python_version >= "2.7" and python_version < "2.8"': ['enum34>=1.1,<2.0']}

setup_kwargs = {
    'name': 'cafeteria',
    'version': '0.18.0',
    'description': 'Cafeteria: A convenience package providing various building blocks enabling pythonic patterns.',
    'long_description': '|pypi| |travis| |black|\n\nPython Cafeteria Package\n========================\n\nA convenience package providing various building blocks for pythonic patterns.\n\n\n.. |pypi| image:: https://badge.fury.io/py/python-cafe.svg\n    :target: https://badge.fury.io/py/python-cafe\n.. |travis| image:: https://travis-ci.org/abn/cafeteria.svg?branch=master\n    :target: https://travis-ci.org/abn/cafeteria\n.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/ambv/black\n',
    'author': 'Arun Babu Neelicattu',
    'author_email': 'arun.neelicattu@gmail.com',
    'url': 'https://github.com/abn/cafeteria',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
}


setup(**setup_kwargs)
