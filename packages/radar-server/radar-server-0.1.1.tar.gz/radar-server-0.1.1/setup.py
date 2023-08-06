# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['radar_server', 'radar_server.fields']

package_data = \
{'': ['*']}

install_requires = \
['vital-tools>=0.1.13,<0.2.0']

setup_kwargs = {
    'name': 'radar-server',
    'version': '0.1.1',
    'description': '',
    'long_description': '# radar-resolver\n\n`poetry add radar-resolver`',
    'author': 'Jared Lunde',
    'author_email': 'jared@BeStellar.co',
    'url': 'https://github.com/jaredLunde/radar-resolver',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
