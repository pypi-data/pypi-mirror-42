======================
Django Static Revision
======================


Provide a context variable to retrieve the version of a Django application.

This variable is meant to change the URL of a static file, to invalidate browser cache.


Install
-------

.. code-block:: shell

    pip3 install dj-static-revision

`Django Static Revision` only supports Python 3.4+.


Usage
-----

Add ``dj_static_revision.context_processors.static_revision`` to your ``context_processors`` list.

.. code-block:: python

    TEMPLATES = (
        {
            'NAME': 'jinja2',
            'BACKEND': 'django_jinja.backend.Jinja2',
            'OPTIONS': {
                'context_processors': (
                    # Other context processors
                    'dj_static_revision.context_processors.static_revision',
                ),

A variable ``REVISION`` will then exists in your template, you can use it to append to static file URL.

.. code-block:: jinja

    <script src="{{ static('js/app.js') }}?v={{ REVISION }}"></script>


`Django Static Revision` retrieves revision string from Git history.
If your source code is not managed by Git, the revision info will be read from a file named `.version` placed next to `manage.py` file.


Settings
--------

The revision string will be truncated to 10 characters. You can change that by add to Django settings:

.. code-block:: python

    STATIC_REVISION_STRING_LENGTH = 10

You can also change the file for `Django Static Revision` to read revision string from, by add this setting:

.. code-block:: python

    STATIC_REVISION_VERSION_FILE = '.version'
