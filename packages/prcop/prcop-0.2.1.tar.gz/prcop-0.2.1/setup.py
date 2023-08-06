# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['prcop']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'requests>=2.21,<3.0']

entry_points = \
{'console_scripts': ['prcop = prcop.cli:cli']}

setup_kwargs = {
    'name': 'prcop',
    'version': '0.2.1',
    'description': 'Send Slack alerts to remind your team when reviews are overdue on pull requests',
    'long_description': '# prcop\n\n[![Build Status](https://travis-ci.org/RobbieClarken/prcop.svg?branch=master)](https://travis-ci.org/RobbieClarken/prcop)\n[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/RobbieClarken/prcop/blob/master/LICENSE)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n\nSend Slack alerts to remind your team when reviews are overdue on pull requests.\n\nCurrently supports self-hosted Bitbucket servers.\n\n## Installation\n\n```\npython3.7 -m pip install prcop\n```\n\n## Usage\n\n```\nprcop run \\\n  --bitbucket-url https://bitbucket.example.com/ \\\n  --slack-webhook https://hooks.slack.com/services/<id> \\\n  --slack-channel development \\\n  project1/repo1 project1/repo2 project2/repo3\n```\n',
    'author': 'RobbieClarken',
    'author_email': 'robbie.clarken@gmail.com',
    'url': 'https://github.com/RobbieClarken/prcop',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
