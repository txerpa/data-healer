============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/txerpa/data-healer/issues

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "feature"
is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

data-healer could always use more documentation, whether as part of the
official data-healer docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/txerpa/data-healer/issues

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `data-healer` for local development.

Operating system requirements:

    * Python
    * `Node <https://nodejs.org/es//>`_

First, set your app's secret key as an environment variable. For example,
add the following to ``.bashrc`` or ``.bash_profile``.

.. code-block:: bash

    export DATA_HEALER_SECRET='something-really-secret'

Run the following commands to bootstrap your environment ::

    git clone https://github.com/txerpa/data-healer
    cd data-healer
    pip install -r requirements/dev.txt

In general, before running shell commands, set the ``FLASK_APP`` and
``FLASK_DEBUG`` environment variables ::

    export FLASK_APP=healer_app.py
    export FLASK_DEBUG=1

To run all tests, run ::

    flask test

Install npm dependencies::

    npm install
    npm start  # run the webpack dev server and flask server using concurrently

Set Node in dev mode::

    export NODE_ENV=development


Deployment
----------

To deploy::

    export FLASK_APP=healer_app.py
    export FLASK_DEBUG=0
    npm run build   # build assets with webpack
    flask run       # start the flask server

In your production environment, make sure the ``FLASK_DEBUG`` environment
variable is unset or is set to ``0``, so that ``ProdConfig`` is used.

