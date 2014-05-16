Change Log
----------

1.0.0 05/15/2014
~~~~~~~~~~~~~~~~
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
