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
    'version': '1.0.1',
    'description': 'Safely creating releases when you change the version number.',
    'long_description': '|CircleCI|_\n\n.. |CircleCI| image:: https://circleci.com/gh/cjw296/carthorse/tree/master.svg?style=shield\n.. _CircleCI: https://circleci.com/gh/cjw296/carthorse/tree/master\n\nCarthorse\n=========\n\nSafely creating releases when you change the version number.\n\nYou use it by adding configuration to a yaml or toml file, and then adding the following\nto your continuous integration pipeline::\n\n    pip install -U carthorse\n    carthorse\n\nTOML Configuration\n------------------\n\nYour file should contain a section such as the following::\n\n    [tool.carthorse]\n    version-from = "poetry"\n    tag-format = "v{version}"\n    when = [\n      "version-not-tagged"\n    ]\n    actions = [\n       { run="poetry publish --username $POETRY_USER --password $POETRY_PASS --build"},\n       { name="create-tag"},\n    ]\n\nThis is designed so that it can be included as part of a ``pyproject.toml`` file.\n\nYAML Configuration\n------------------\n\nYour file should contain a section such as the following::\n\n    carthorse:\n      version-from: poetry\n      tag-format: v{version}\n      when:\n        - version-not-tagged\n      actions:\n        - run: "poetry publish --username $POETRY_USER --password $POETRY_PASS --build"\n        - create-tag\n\nWhat does it do?\n----------------\n\nRoughly speaking:\n\n- Extract your project\'s version from its source code.\n- Format a tag based on the version\n- Perform a number of checks, if any of those fail, stop.\n- Perform any actions you specify.\n\nVersion extraction\n------------------\n\nThe following methods of extracting the version of a project are currently supported:\n\n``poetry``\n  This will parse a project\'s ``pyproject.toml`` and use the ``tool.poetry.version``\n  key as the version for the project.\n\nTag formatting\n--------------\n\nThe ``tag-format`` configuration option lets you control the format of the version tag\nby specifying a python format string into which the version will be interpolated.\nThe default is ``v{version}``.\n\nPerforming checks\n-----------------\n\nEach check in the ``when`` configuration section will be performed in order. If any fail\nthen no actions will be performed.\n\nThe following checks are currently available:\n\n``version_not_tagged``\n  This will pass if no current git tag exists for the version extracted from the poject.\n\n``never``\n  A safety net and testing helper, this check will never pass.\n\nActions\n-------\n\nIf all the checks pass, then the actions listed are executed in order. If an error occurs\nduring the execution of an action, no further actions will be executed.\n\nThe following actions are currently available:\n\n``run``\n  The the specified command in a shell. The full environment will be passed through and\n  ``$TAG`` will contain the tag computed from the tag format.\n\n``create_tag``\n  This will create a git tag for the computed tag based on the extracted version and push\n  it to the specified remote. By default, the ``origin`` remote is used.\n\n1.0.1 (27 Feb 2019)\n-------------------\n\n- Better PyPI metadata.\n\n1.0.0 (27 Feb 2019)\n-------------------\n\n- First release, supporting poetry and git tagging.\n',
    'author': 'Chris Withers',
    'author_email': 'chris@withers.org',
    'url': 'https://github.com/cjw296/carthorse',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
