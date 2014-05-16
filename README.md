python-ccuapi
=============

Python wrapper around Akamai ccuapi

Hat tip to https://github.com/beathan/django-akamai for inspiring the original code.

## Credentials

Credentials can be provided in 1 of 3 ways:

1. AKAMAI_USERNAME and AKAMAI_PASSWORD environment variables.
2. A `.akamai` config file in the user's home directory. [(Sample config included as .akamai.sample)](https://github.com/dryan/python-ccuapi/blob/master/.akamai.sample)
3. Passing `username` and `password` kwargs to ccuapi.purge.PurgeRequest on initialization.

## Email Notifications

One or more comma-separated email addresses may be set to receive notifications
when a content purge is complete. These are provided in 1 of 3 ways:

1. AKAMAI_NOTIFY_EMAIL environment variable.
2. In the `.akamai` config file.
3. Passing `email` kwarg to ccuapi.purge.PurgeRequest on initialization.

## Usage

	from ccuapi.purge import PurgeRequest
	purger	= 	PurgeRequest()
	purger.add('http://domain.com') # this can be a string, or list of strings
	results	= 	purger.purge() # returns the status of the request
	
## Command Line Usage

	ccu_purge http://domain.com
	
Run `ccu_purge -h` for additional options.

## Using a proxy server?
ccuapi_purge will honor the standard proxy environment variables so if you
are running behind a proxy export the proper environment variables:

    $ export HTTP_PROXY="http://10.10.1.10:8080"
    $ export HTTPS_PROXY="http://10.10.1.10:8080"
