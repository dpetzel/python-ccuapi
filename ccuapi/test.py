"""
Unit tests for python ccuapi
"""

from unittest import TestCase

from httmock import HTTMock, all_requests

from .purge import PurgeRequest

from .exceptions import AkamaiAuthorizationException
from .exceptions import AkamaiArlPurgeWithoutUrls
from .exceptions import AkamaiStatusRequestWithoutPurge
from .exceptions import AkamaiPurgeTypeException
from .exceptions import AkamaiCredentialException
from .exceptions import AkamaiAuthenticationException


# pylint: disable=too-many-public-methods
class CcuapiTest(TestCase):
    """
    Test case holding Unit tests for the ccuapi package
    """
    def setUp(self):
        # self.purger = PurgeRequest(kind='arl', username='unitest',
        #                               password='unitest')
        self.purger = PurgeRequest(kind='arl')

    def test_demands_valid_purge_type(self):
        """
        Ensures that the class with enforce someone passing in the type/kind
        of purge to do
        """
        with self.assertRaises(AkamaiPurgeTypeException):
            PurgeRequest()

    def test_demands_a_username(self):
        """Ensure a username is requred"""
        with self.assertRaises(AkamaiCredentialException):
            PurgeRequest(kind='arl', username=None)

    def test_demands_a_password(self):
        """Ensure a password is required"""
        with self.assertRaises(AkamaiCredentialException):
            PurgeRequest(kind='arl', username='unitest', password=None)

    def test_urls_via_constructor(self):
        """
        Ensure URLs list passed via the constructor are processed
        """
        purger = PurgeRequest(kind='arl', username='unitest',
                              password='unitest',
                              urls=['http://my.domain.com/url1',
                                    'http://my.domain.com/url2'])

        self.assertIn('http://my.domain.com/url1', purger.urls)
        self.assertIn('http://my.domain.com/url2', purger.urls)

    def test_urls_via_add_method(self):
        """
        Ensure the add method of the PurgeRequest object accepts supported
        types.
        """
        self.purger.add('http://my.domain.com/url1')
        self.purger.add(['http://my.domain.com/url2'])

        # Picking some random type that shouldn't ever be valid in the future
        with self.assertRaises(TypeError):
            self.purger.add(Exception)

        self.assertIn('http://my.domain.com/url1', self.purger.urls)
        self.assertIn('http://my.domain.com/url2', self.purger.urls)

    def test_queue_length_lookup(self):
        """
        Ensure we can lookup the queue length
        """
        with HTTMock(mock_lookup_queue_length):
            self.assertEqual(self.purger.queue_length(), 100)

    def test_purge_with_failed_auth(self):
        """
        Ensure we raise the proper type of exception when authentication failed
        """
        self.purger.add('http://my.domain.com/url1')
        with HTTMock(mock_purge_bad_creds):
            with self.assertRaises(AkamaiAuthenticationException):
                self.purger.purge()

    def test_purge_failed_authorization(self):
        """
        Ensure we raise the proper type of exception when authorization fails
        """
        self.purger.add('http://my.domain.com/url1')
        with HTTMock(mock_purge_unauth_url):
            with self.assertRaises(AkamaiAuthorizationException):
                self.purger.purge()

    def test_purge_method(self):
        """
        The meat of the whole thing... make sure it purges
        """
        self.purger.add('http://my.domain.com/url1')
        with HTTMock(mock_purge_success):
            self.purger.purge()
            # test the varios attributes that should be exposed
            attr_map = {
                'estimated_seconds': 420,
                'progress_uri': '/ccu/v2/purges/1234-456-7890',
                'purge_id': '1234-456-7890',
                'support_id': '123456789',
                'http_status': 201,
                'detail': 'Request accepted.',
                'ping_after_seconds': 420
            }
            for key, value in attr_map.items():
                current = getattr(self.purger, key)
                expected = value
                self.assertEqual(current, expected)

    def test_status_before_purge(self):
        """
        Test the behaviour if status is called before a purge is issued
        """
        with self.assertRaises(AkamaiStatusRequestWithoutPurge):
            self.purger.status()

    def test_status_of_current_purge(self):
        """
        Ensure we can call status without a purge_id and it returns the status
        for the instance
        """
        self.purger.add('http://my.domain.com/url1')
        with HTTMock(mock_purge_success):
            self.purger.purge()

        # Now that we created the purge request, check its status
        with HTTMock(mock_status_1234):
            status = self.purger.status()
            self.assertEqual(status['purgeId'], '1234-456-7890')

    def test_status_of_alternate_purge(self):
        """
        Ensure if we pass a purge_id that is different than the id of the
        current id it will look it up
        """
        with HTTMock(mock_status_987):
            status = self.purger.status(purge_id='987')
            self.assertEqual(status['purgeId'], '987')

    def test_arl_purge_without_urls(self):
        """
        When doing an arl (URL) type purge and no urls are passed
        """
        with self.assertRaises(AkamaiArlPurgeWithoutUrls):
            self.purger.purge()

# Define all the mocks we need here. We are disabling unused-argument for
# pylint on all the mocks. The way httmock works we have to mimic the
# signature with url, request, but we never use them. We disable it once
# at the top of this section rather than on each mock.

# In addition to the the args issue pep8 and pylint seem to disagree on
# the continuation so favor pep8


# pylint: disable=unused-argument, bad-continuation
@all_requests
def mock_lookup_queue_length(url, request):
    """
    Mocks an API call to check the queue length
    """
    return {'status_code': 200,
            'content-type': 'application/json',
            'server': 'Apache',
            'content': {
                "supportId": "123456789",
                "httpStatus": 200,
                "detail": "The queue may take a minute to reflect new or "
                          "removed requests.",
                "queueLength": 100}
            }


@all_requests
def mock_purge_success(url, request):
    """
    Mock a success Purge request
    """
    return {'status_code': 201,
            'content-type': 'application/json',
            'server': 'Apache',
            'content-location': '/ccu/v2/purges/1234-456-7890',
            'content': {
                "estimatedSeconds": 420,
                "progressUri": "/ccu/v2/purges/1234-456-7890",
                "purgeId": "1234-456-7890",
                "supportId": "123456789",
                "httpStatus": 201,
                "detail": "Request accepted.",
                "pingAfterSeconds": 420}
            }


@all_requests
def mock_purge_unauth_url(url, request):
    """
    Mock a purge request in which the credentials are valid, but the
    url that was requested is not allowed
    """
    return {'status_code': 403,
            'content-type': 'application/json',
            'server': 'Apache',
            'content': {
                "supportId": "123456789",
                "title": "unauthorized arl",
                "httpStatus": 403,
                "detail": "http://www.example.com/bogus",
                "describedBy": "https://api.ccu.akamai.com/ccu/v2/errors/"
                               "unauthorized-arl"}
            }


@all_requests
def mock_purge_bad_creds(url, request):
    """
    Mocks a response of a purge issued with invalid credentials. In this
    situation we will get a text/html response regardless of if we send
    a content-type header of json, so the content type in this response
    of html is not a typo
    """
    return {'status_code': 401,
            'content-type': 'text/html;charset=utf-8',
            'server': 'Apache',
            'www-authenticate': 'Basic realm="Luna Control Center"',
            'content': '<html><head><title>401 Unauthorized</title></head>'
                       '<body><p>401 Unauthorized</p><p>You are not authorized'
                       ' to access that resource</p></body></html>'
            }


@all_requests
def mock_status_1234(url, request):
    """
    Mock a status lookup for a purge request with an id of 1234...

    This mock is intended to go hand in hand with mock_purge_success
    and its ID 1234-456-7890
    """
    return {'status_code': 200,
            'content-type': 'application/json',
            'server': 'Apache',
            'content': {
                "originalEstimatedSeconds": 420,
                "progressUri": "/ccu/v2/purges/1234-456-7890",
                "originalQueueLength": 0,
                "purgeId": "1234-456-7890",
                "supportId": "123456789",
                "httpStatus": 200,
                "completionTime": None,
                "submittedBy": "myself",
                "purgeStatus": "In-Progress",
                "submissionTime": "2014-05-10T20:50:36Z",
                "pingAfterSeconds": 60}
            }


@all_requests
def mock_status_987(url, request):
    """
    Mock a status lookup for a purge request with an id of 987
    """
    return {'status_code': 200,
            'content-type': 'application/json',
            'server': 'Apache',
            'content': {
                "originalEstimatedSeconds": 420,
                "progressUri": "/ccu/v2/purges/987",
                "originalQueueLength": 0,
                "purgeId": "987",
                "supportId": "987654321",
                "httpStatus": 200,
                "completionTime": None,
                "submittedBy": "myself",
                "purgeStatus": "In-Progress",
                "submissionTime": "2014-05-09T20:50:36Z",
                "pingAfterSeconds": 60}}
