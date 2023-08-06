# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['radar_server', 'radar_server.fields']

package_data = \
{'': ['*']}

install_requires = \
['trie-memoize>=0.1.1,<0.2.0']

entry_points = \
{'console_scripts': ['bench = bench:main', 'tests = tests:main']}

setup_kwargs = {
    'name': 'radar-server',
    'version': '0.1.3',
    'description': '',
    'long_description': '# radar-server\n\n`poetry add radar-server`\n',
    'author': 'Jared Lunde',
    'author_email': 'jared@BeStellar.co',
    'url': 'https://github.com/jaredLunde/radar-server',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
