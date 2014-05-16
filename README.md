python-ccuapi
=============

Python wrapper around Akamai ccuapi

Hat tip to https://github.com/beathan/django-akamai for inspiring the code.

## Credentials

Credentials can be provided in 1 of 3 ways:

1. AKAMAI_USERNAME and AKAMAI_PASSWORD environment variables.
2. A `.akamai` config file in the user's home directory. [(Sample config included as .akamai.sample)](https://github.com/dryan/python-ccuapi/blob/master/.akamai.sample)
3. Passing `username` and `password` kwargs to ccuapi.purge.PurgeRequest on initialization.

## Email Notifications

One or more comma-separated email addresses may be set to receive notifications when a content purge is complete. These are provided in 1 of 3 ways:

1. AKAMAI_NOTIFY_EMAIL environment variable.
2. In the `.akamai` config file.
3. Passing `email` kwarg to ccuapi.purge.PurgeRequest on initialization.

## Usage

	from ccuapi.purge import PurgeRequest
	purger	= 	PurgeRequest()
	purger.add('http://domain.com') # this can be a string, list of strings, Django QuerySet or Django object with the `get_absolute_url` method defined
	results	= 	purger.purge() # returns a list of responses from Akamai, 1 per 100 URLs sent
	
## Command Line Usage

	ccu_purge http://domain.com
	
Run `ccu_purge -h` for additional options.

## Using a proxy server?

If you're using this library on a server that uses an http/https proxy, you'll likely hit  `Connection Timeout` issues
because suds ignores the environment proxy variables, as [described here](http://stackoverflow.com/questions/12414600/suds-ignoring-proxy-setting).

One simple solution:

    #Hat tip: http://stackoverflow.com/questions/12414600/suds-ignoring-proxy-setting
    from suds.transport.http import HttpTransport as SudsHttpTransport
    class EnvProxyHonoringTransport(SudsHttpTransport):
        def u2handlers(self):
            return []

    purger = PurgeRequest(...)
    purger.client.set_options(transport = EnvProxyHonoringTransport())
