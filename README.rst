python-ccuapi
=============

.. image:: https://travis-ci.org/dpetzel/python-ccuapi.svg?branch=master
    :target: https://travis-ci.org/dpetzel/python-ccuapi
.. image:: https://api.shippable.com/projects/5376cb16a5c0d1f801e953ae/badge/master
    :target: https://www.shippable.com/projects/5376cb16a5c0d1f801e953ae

Python wrapper around Akamai ccuapi including a command line utility

Requirements
------------
Python 2.7, 3.2, 3.3, and 3.4 are currently required. There are currently no plans
to support anything older than Python 2.7

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

Change Log
----------
1.1.2 (05/23/2014)
~~~~~~~~~~~~~~~~~~

* Fix bug where purge method was returning the results of a status call
  rather than the actual results of the purge

1.1.1 (05/22/2014)
~~~~~~~~~~~~~~~~~~

* Fix entry point issue with CLI running

1.1.0 (05/16/2014)
~~~~~~~~~~~~~~~~~~

* Python 3 support
* Catch exception in CLI when no username is supplied

1.0.0 (05/15/2014)
~~~~~~~~~~~~~~~~~~
This versions marks a fairly significant overhaul to convert to Akamai's REST
based API. There some backward incompatible changes so be sure to review the
list of changes below:

* Drop Django related code. A separate Django module should be created which
  can potentially leverage this library, however having Django related code
  in this module didn't fit well.
* Unittests have been introduced which should make future updates safer
* Pylint and PEP8 compliance
* WSDL has been dropped. Since Akamai won't be supporting use of the SOAP API
  going forward, there was no reason to keep this around
* Project is now tested using Travis-CI

0.5.0
~~~~~
This was the last version which supported the SOAP based API