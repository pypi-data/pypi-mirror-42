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
    'version': '0.1.1',
    'description': 'A memoization algorithm in which each function argument represents a new key, creating a trie of caches as defined by your setup.',
    'long_description': '# trie-memoize\n\n`poetry add trie-memoize`',
    'author': 'Jared Lunde',
    'author_email': 'jared@BeStellar.co',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.3,<4.0',
}


setup(**setup_kwargs)
