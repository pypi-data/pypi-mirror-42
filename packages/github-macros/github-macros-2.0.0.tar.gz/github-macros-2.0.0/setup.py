# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['github_macros', 'github_macros.cli', 'github_macros.models']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8.0,<3.0.0',
 'requests>=2.21.0,<3.0.0',
 'sh>=1.12.14,<2.0.0']

entry_points = \
{'console_scripts': ['gh-permit = github_macros.cli.repo_permissions:main',
                     'gh-protect = github_macros.cli.branch_protection:main',
                     'gh-refresh = github_macros.cli.refresh:main',
                     'gh-releases = github_macros.cli.releases:main']}

setup_kwargs = {
    'name': 'github-macros',
    'version': '2.0.0',
    'description': '',
    'long_description': None,
    'author': 'David Alexander',
    'author_email': 'opensource@thelonelyghost.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
