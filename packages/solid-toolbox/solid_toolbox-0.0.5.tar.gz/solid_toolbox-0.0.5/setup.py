# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['solid_toolbox']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'prettytable==0.7.2', 'solidpython>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'solid-toolbox',
    'version': '0.0.5',
    'description': 'A collection of utilities for solidpython',
    'long_description': '# Solid toolbox\n\nA collection of utilities for [SolidPython](https://github.com/SolidCode/SolidPython).\n\n',
    'author': 'Michael Lee',
    'author_email': 'michael.lee.0x2a@gmail.com',
    'url': 'https://github.com/michael0x2a/solid_toolbox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
