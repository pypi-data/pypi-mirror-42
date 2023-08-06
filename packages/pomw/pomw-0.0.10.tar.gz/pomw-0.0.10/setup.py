# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pomw', 'pomw.console', 'pomw.model']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.7,<3.0',
 'semver>=2.8,<3.0',
 'taskw>=1.2,<2.0',
 'timew>=0.0.18,<0.0.19',
 'unijson>=1.0,<2.0',
 'urwid>=2.0,<3.0']

entry_points = \
{'console_scripts': ['pomw = pomw.console:main']}

setup_kwargs = {
    'name': 'pomw',
    'version': '0.0.10',
    'description': 'The Pomodoro Technique using TaskWarrior and TimeWarrior',
    'long_description': '# Pomodorowarrior #\n\nA command line tool that integrates with Taskwarrior and Timewarrior to implement the Pomodoro Technique.\n\n## Command Line Interface ##\n\nPomodorowarrior uses a command with subcommands interface, similar to Taskwarrior itself. commands can be broken up into 3 different pomodoro phases.\n\n**Planning**\n\n```bash\n# Plan a new pomodoro\npomw plan TASK_ID [-d DATE] [-q QUANTITY]\n``` \n\n**Recording**\n\n```bash\n# Mark a pomodoro as completed\npomw complete TASK_ID [-e END_TIME]`\n\n# Mark an internal or external interruption\npomw interrupt TASK_ID {internal|external}\n\n# Void a pomodoro\npomw void TASK_ID\n\n# Add non pomodoro time\npomw nonpom TASK_ID [-q QUANTITY] [-d DURATION] [-s START_TIME] [-e END_TIME]\n```\n\n**Reporting**\n\n```bash\n# Print the To Do Today sheet\npomw tdt\n```\n\n\n## Special notation for quantities ##\n\nTo reduce the number of subcommands needed by the CLI (`unplan` or `delete` commands for example), I implemented a special notation for the `QUANTITIES` arguments\n\n```\n+X => Current value = Current value + X\n-X => Current value = Current value - X\n X => Current value = X\n```\n\nFor example if you look at the following series of commands:\n\n```\npomw plan 2 -q 1\n# Planned pomodoros for task 2 is 1\npomw plan 2 -q +1\n# Planned pomodoros for task 2 is 2\npomw plan 2 -q 1\n# Planned pomodoros for task 2 is 1\npomw plan 2 -q -1\n# Planned pomodoros for task 2 is 0\n```\n\n## Configuration ##\n\nThe configuration file should be located at `$HOME/.config/pomw/pomwrc`\n\nThis example shows the supported configuration values\n\n```\n[pomodoro]\n# Pomodoro length in minutes\nlength = 30\n\n[timew]\n# Should pomw sync values to Time Warrior\nsync = False\n```\n\n## Taskwarrior and Timewarrior integration ##\n\nPomodorowarrior never mark tasks as completed in Taskwarrior, it only adds Pomodoros to a task. \nEvery time a Pomodoro gets marked as completed, the time is logged in Timewarrior.\n\n# Development #\n\n## Build System ##\n\nStarting with `0.0.3` we replace [setuptools](https://setuptools.readthedocs.io) with [poetry](https://poetry.eustace.io).\nPoetry is [PEP 518](https://www.python.org/dev/peps/pep-0518/) compliant, and uses `pyproject.toml` for configuration. In my opinion it provides for a simpler development experience.\n\nPoetry recommends that you install it isolated from the rest of your system. This can be done by running the install script:\n\n`curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python`\n\n## Release ##\n\nThe script `./release.py` have been developed to automate cutting releases. It requires [git-extras](https://github.com/tj/git-extras) to be installed on your system.\n\nIf you want to manually create a release, you have to follow these rules:\n\n- Only release from `master`\n- Update `pomw/__version__.py` with the new version number\n- Update `pyproject.toml` with the new version number\n- Update `Changelog` with the commits since the previous release\n\n## Upload a release to PYPI ##\n\nOnce a tag is created, and pushed to Gitlab, the release is automatically uploaded to PYPI by the Gitlab CI publish stage.\n\n## TODO ##\n\n- Implement more reports\n- Tracking pomodoros using the interactive user interface\n\n',
    'author': 'Tjaart van der Walt',
    'author_email': 'tjaart@tjaart.org',
    'url': 'https://tjaart.gitlab.io/pomw',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
