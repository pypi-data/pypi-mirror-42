# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['carthorse']

package_data = \
{'': ['*']}

install_requires = \
['pyyaml>=3.13,<4.0', 'toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['carthorse = carthorse.cli:main']}

setup_kwargs = {
    'name': 'carthorse',
    'version': '0.1.0',
    'description': 'Safely creating releases when you change the version number.',
    'long_description': None,
    'author': 'Chris Withers',
    'author_email': 'chris@withers.org',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
