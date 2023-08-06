# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['wirecard']

package_data = \
{'': ['*']}

install_requires = \
['glom>=19.2,<20.0', 'requests>=2.21,<3.0']

setup_kwargs = {
    'name': 'wirecard',
    'version': '0.1.1',
    'description': '',
    'long_description': '# Wirecard\n',
    'author': 'Jonatas Baldin',
    'author_email': 'jonatas.baldin@gmail.com',
    'url': 'https://github.com/Flickswitch/wirecard',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
