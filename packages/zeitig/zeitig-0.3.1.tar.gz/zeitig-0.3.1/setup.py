# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['zeitig']

package_data = \
{'': ['*'], 'zeitig': ['templates/*']}

install_requires = \
['click',
 'colorama',
 'crayons',
 'dateparser',
 'jinja2',
 'pendulum',
 'qtoml>=0.2.4,<0.3.0']

entry_points = \
{'console_scripts': ['z = zeitig.scripts:run']}

setup_kwargs = {
    'name': 'zeitig',
    'version': '0.3.1',
    'description': 'time tracker and reporter',
    'long_description': None,
    'author': 'Oliver Berger',
    'author_email': 'diefans@gmail.com',
    'url': 'https://github.com/diefans/zeitig',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
