# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pupy']

package_data = \
{'': ['*']}

install_requires = \
['msgpack>=0.6.1,<0.7.0']

setup_kwargs = {
    'name': 'pupy',
    'version': '2.3.4',
    'description': 'pretty useful python',
    'long_description': None,
    'author': 'jessekrubin',
    'author_email': 'jessekrubin@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
