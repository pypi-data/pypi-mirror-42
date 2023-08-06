# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pomw', 'pomw.model']

package_data = \
{'': ['*']}

install_requires = \
['argcomplete>=1.9,<2.0',
 'python-dateutil>=2.7,<3.0',
 'semver>=2.8,<3.0',
 'taskw>=1.2,<2.0',
 'timew>=0.0.18,<0.0.19',
 'unijson>=1.0,<2.0',
 'urwid>=2.0,<3.0']

setup_kwargs = {
    'name': 'pomw',
    'version': '0.0.7',
    'description': 'The Pomodoro Technique using TaskWarrior and TimeWarrior',
    'long_description': None,
    'author': 'Tjaart van der Walt',
    'author_email': 'tjaart@tjaart.org',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
