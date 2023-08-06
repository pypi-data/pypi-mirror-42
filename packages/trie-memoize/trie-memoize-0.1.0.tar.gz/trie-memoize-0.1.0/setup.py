# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['trie_memoize']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['tests = tests:main']}

setup_kwargs = {
    'name': 'trie-memoize',
    'version': '0.1.0',
    'description': '',
    'long_description': '# trie-memoize\n\n`poetry add trie-memoize`',
    'author': 'Jared Lunde',
    'author_email': 'jared.lunde@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
