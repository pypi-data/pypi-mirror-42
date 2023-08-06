# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pycorreios3']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.19,<3.0', 'zeep>=3.1,<4.0']

setup_kwargs = {
    'name': 'pycorreios3',
    'version': '1.2.2',
    'description': 'Acesso facil a todos os web services dos correios.',
    'long_description': '',
    'author': 'Marcelo Bello',
    'author_email': 'mbello@users.noreply.github.com',
    'url': 'https://github.com/mbello/pycorreios3',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
