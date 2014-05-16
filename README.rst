python-ccuapi
=============

.. image:: https://travis-ci.org/dpetzel/python-ccuapi.svg?branch=master
    :target: https://travis-ci.org/dpetzel/python-ccuapi

Python wrapper around Akamai ccuapi including a command line utility

Requirements
------------
Currently only Python 2.7 is supported. There are plans to make it work on
Python 3 however.

* `Requests <http://docs.python-requests.org/en/latest/>`_

Credentials
-----------
Credentials can be provided in 1 of 3 ways:

#. AKAMAI_USERNAME and AKAMAI_PASSWORD environment variables.
#. A `.akamai` config file in the user's home directory.
   Example: https://github.com/dpetzel/python-ccuapi/blob/master/.akamai.sample
#. Passing `username` and `password` kwargs to ccuapi.purge.PurgeRequest
   on initialization.

Email Notifications
-------------------
One or more comma-separated email addresses may be set to receive notifications
when a content purge is complete. These are provided in 1 of 3 ways:

#. AKAMAI_NOTIFY_EMAIL environment variable.
#. In the `.akamai` config file
#. Passing `email` kwarg to ccuapi.purge.PurgeRequest on initialization.

Usage
-----
.. code-block:: python

    from ccuapi.purge import PurgeRequest
    purger = PurgeRequest()
    purger.add('http://domain.com') # this can be a string, or list of strings
    results = purger.purge() # returns the status of the request

Command Line Usage
------------------
.. code-block:: bash

    ccu_purge http://domain.com

Run `ccu_purge -h` for additional options.

Using a proxy server
--------------------
ccuapi_purge will honor the standard proxy environment variables so if you
are running behind a proxy export the proper environment variables:

.. code-block:: bash

    $ export HTTP_PROXY="http://10.10.1.10:8080"
    $ export HTTPS_PROXY="http://10.10.1.10:8080"

.. include:: CHANGELOG.rst