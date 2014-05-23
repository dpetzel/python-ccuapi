"""
This module holds the class(es) required to interact with the Akamai
CCU API.
"""

from . import AKAMAI_USERNAME, AKAMAI_PASSWORD, AKAMAI_NOTIFY_EMAIL
from . import AKAMAI_API_HOST

from .exceptions import AkamaiPurgeTypeException
from .exceptions import AkamaiCredentialException
from .exceptions import AkamaiAuthenticationException
from .exceptions import AkamaiAuthorizationException
from .exceptions import AkamaiArlPurgeWithoutUrls
from .exceptions import AkamaiStatusRequestWithoutPurge

import requests
import json
import re


# pylint: disable=too-many-instance-attributes
class PurgeRequest(object):
    """
    Represents a request to purge content from the Akamai network
    """
    # pylint: disable=too-many-arguments
    def __init__(self, username=AKAMAI_USERNAME, password=AKAMAI_PASSWORD,
                 email=AKAMAI_NOTIFY_EMAIL, options=None, urls=None,
                 kind=None, domain='production'):

        # Start by validating input
        if kind not in ['arl', 'cpcode']:
            raise AkamaiPurgeTypeException(
                "{0} is not a valid purge type."
                " Must be arl or cpcode".format(kind))

        # currently cpode based purges are not supported. There isn't any
        # reason not to implement them, other than I didn't have the ability
        # to test it when reworking to the rest API
        if kind == 'cpcode':
            raise NotImplementedError(
                "Support for CP Code purges is not currently implemented")

        if not username:
            raise AkamaiCredentialException('Username not provided')
        self.password = password
        if not password:
            raise AkamaiCredentialException('Password not provided')

        self.type = kind
        self.domain = domain
        self.username = username
        self.password = password
        self.email = email

        # This set of attributes will get populated after a success purge
        self.estimated_seconds = None
        self.progress_uri = None
        self.purge_id = None
        self.support_id = None
        self.http_status = None
        self.detail = None
        self.ping_after_seconds = None

        self.urls = set()
        if urls is not None:
            self.add(urls)

        self.email = email

        self.options = {
            'email-notification-name':  self.email,
            'action':                   'remove',
            'type':                     self.type,
            'domain':                   self.domain,
        }
        if options:
            self.options.update(options)

    def _call_api(self, path, method='POST', payload=None):
        """
        Make a call to the Akamai API

        :Parameters:
            path : String
                The path portion of the api url to call. This will be combined
                with the base URL
            payload : Dictionary or String
                Pass a dictionary when passing key/value pairs, or a plain
                string if passing raw post data
        """
        api_url = "https://{0}{1}".format(AKAMAI_API_HOST, path)
        api_client = requests.Session()
        api_client.auth = (self.username, self.password)
        api_client.headers.update({'Content-Type': 'application/json'})

        if payload is not None and type(payload) == dict:
            payload = json.dumps(payload)

        if method == 'GET':
            rsp = api_client.get(api_url)
        else:
            rsp = api_client.post(api_url, data=payload)

        if rsp.status_code == 401:
            raise AkamaiAuthenticationException(
                'Failed to authenticate to Akamai API. Please double check'
                ' your username and password')
        elif rsp.status_code == 403:
            raise AkamaiAuthorizationException(
                'It appears you may not have access to perform this operation'
                ' on this object/endpoint. Please confirm your permissions'
            )
        else:
            return rsp

    def add(self, urls):
        """
        Add one or more URLs to be purged
        """

        if isinstance(urls, list):
            for url in urls:
                self.urls.add(url)
        elif isinstance(urls, str):
            self.urls.add(urls)
        else:
            raise TypeError("urls must be a string, or list of strings")

    def purge(self):
        """
        Do the actual work of issuing the purge request
        """
        if self.type == "arl" and len(self.urls) < 1:
            raise AkamaiArlPurgeWithoutUrls(
                "You need to supply one or more URLs to purge")
        payload = {'type': self.type, 'domain': self.domain,
                   'objects': list(self.urls)}
        uri = '/ccu/v2/queues/default'
        rsp = self._call_api(uri, payload=payload)
        # In addition to returning the response info
        # use it to populate attributes on the request
        # object, allowing callers to use either
        for key, value in rsp.json().items():
            key_name = camel_to_snake(key)
            setattr(self, key_name, value)

        return rsp.json()

    def queue_length(self):
        """
        allows you to check the approximate number of outstanding purge
        requests in your purge request queue.
        """
        uri = '/ccu/v2/queues/default'
        return int(self._call_api(uri, method='GET').json()['queueLength'])

    def status(self, purge_id=None):
        """
        Lookup the current status of a Purge Request

        The status check defaults to using the ID of the current instance,
        however it does accept an optional purge_id parameter if you wanted
        to look up some other purge request

        Returns a dict representing the JSON return in the status API response
        """
        # progress_uri is an attribute that is added once the purge has been
        # submitted. Before that it will not exist.
        if purge_id is not None:
            uri = "/ccu/v2/purges/{0}".format(purge_id)
        else:
            purge_id = getattr(self, 'purge_id', None)
            uri = getattr(self, 'progress_uri', None)

        # If the caller is not supplying a purge ID its presumed they
        # want to use the ID of the current instance. That value
        # can't exist until purge has been called at least once
        if purge_id is None:
            raise AkamaiStatusRequestWithoutPurge(
                "You need to call the purge method first, or supply a value"
                " for purge_id")

        return self._call_api(uri, method='GET').json()


def camel_to_snake(string):
    """
    This method is a simple little helper to take property names we get back
    from the Akamai API in camelCase to snake_case
    """
    string = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    string = re.sub('(.)([0-9]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', string).lower()
