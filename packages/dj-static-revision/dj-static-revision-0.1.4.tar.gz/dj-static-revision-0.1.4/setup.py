# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dj_static_revision']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.0,<3.0', 'dulwich>=0.19.11,<0.20.0']

setup_kwargs = {
    'name': 'dj-static-revision',
    'version': '0.1.4',
    'description': 'Revision info for Django static file',
    'long_description': '======================\nDjango Static Revision\n======================\n\n\nProvide a context variable to retrieve the version of a Django application.\n\nThis variable is meant to change the URL of a static file, to invalidate browser cache.\n\n\nInstall\n-------\n\n.. code-block:: shell\n\n    pip3 install dj-static-revision\n\n`Django Static Revision` only supports Python 3.4+.\n\n\nUsage\n-----\n\nAdd ``dj_static_revision.context_processors.static_revision`` to your ``context_processors`` list.\n\n.. code-block:: python\n\n    TEMPLATES = (\n        {\n            \'NAME\': \'jinja2\',\n            \'BACKEND\': \'django_jinja.backend.Jinja2\',\n            \'OPTIONS\': {\n                \'context_processors\': (\n                    # Other context processors\n                    \'dj_static_revision.context_processors.static_revision\',\n                ),\n\nA variable ``REVISION`` will then exists in your template, you can use it to append to static file URL.\n\n.. code-block:: jinja\n\n    <script src="{{ static(\'js/app.js\') }}?v={{ REVISION }}"></script>\n\n\n`Django Static Revision` retrieves revision string from Git history.\nIf your source code is not managed by Git, the revision info will be read from a file named `.version` placed next to `manage.py` file.\n\n\nSettings\n--------\n\nThe revision string will be truncated to 10 characters. You can change that by add to Django settings:\n\n.. code-block:: python\n\n    STATIC_REVISION_STRING_LENGTH = 10\n\nYou can also change the file for `Django Static Revision` to read revision string from, by add this setting:\n\n.. code-block:: python\n\n    STATIC_REVISION_VERSION_FILE = \'.version\'\n',
    'author': 'Nguyễn Hồng Quân',
    'author_email': 'ng.hong.quan@gmail.com',
    'url': 'https://bitbucket.org/hongquan/dj-static-revision/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
