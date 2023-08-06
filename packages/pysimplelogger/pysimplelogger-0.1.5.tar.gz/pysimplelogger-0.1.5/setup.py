# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pysimplelogger']

package_data = \
{'': ['*']}

install_requires = \
['pyrandomtools>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'pysimplelogger',
    'version': '0.1.5',
    'description': 'Simple Logger based on python logging',
    'long_description': None,
    'author': 'Rick Alm',
    'author_email': 'rickealm@gmail.com',
    'url': 'http://github.com/rickalm/pysimplelogger',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3,<4',
}


setup(**setup_kwargs)
