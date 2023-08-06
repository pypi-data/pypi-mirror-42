=============================
Django SFTP Server
=============================

.. image:: https://badge.fury.io/py/django-sftp.svg
    :target: https://badge.fury.io/py/django-sftp

.. image:: https://travis-ci.org/vahaah/django-sftp.svg?branch=master
    :target: https://travis-ci.org/vahaah/django-sftp

.. image:: https://codecov.io/gh/vahaah/django-sftp/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/vahaah/django-sftp

SFTP server application that used user authentication of Django.

Documentation
-------------

The full documentation is at https://django-sftp.readthedocs.io.

Quickstart
----------

Install Django SFTP Server::

    pip install django-sftp

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_sftp',
        ...
    )


Generate RSA key

.. code-block:: bash

     ssh-keygen -t rsa -b 4096 -C "your_email@example.com" -m PEM

Run SFTP server

.. code-block:: bash

     ./manage.py sftpserver :11121 -k /tmp/rsa

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
