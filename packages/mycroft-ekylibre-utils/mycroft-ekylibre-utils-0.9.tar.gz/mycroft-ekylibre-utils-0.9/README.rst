Ekylibre set of tools for MycroftAI
====================================

This package is used in our skills for MycroftAI.
It provides access to Ekylibre API and much more...

This is a work in progress...

Packaging for PyPi
------------------

Creates the virtual environment (you need Pipenv):

.. code-block:: bash

    $ pipenv install

Creates packages :

.. code-block:: bash

    $ pipenv run python setup.py sdist bdist_wheel

Publish package to PyPi
-----------------------

Now it's time to publish :

.. code-block:: bash

    $ pipenv run twine upload dist/*


Usage
-----

To install the package, simply:

.. code-block:: bash

    $ pip install mycroft-ekylibre-utils

Mycroft settings
----------------

This package works with a custom config section in your :code:`mycroft.conf` file:

.. code-block:: json

    "ekylibre_api": {
        "host": "yourfarm.ekylibre.farm",
        "user": "you@example.org",
        "password": "*******"
    }