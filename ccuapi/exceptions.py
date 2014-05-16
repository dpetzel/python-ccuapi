"""
Exceptions for the CCUAPI Package
"""


class CcuapiException(Exception):
    """
    Base exception from which all exceptions in this module
    should be raised
    """
    pass


class AkamaiException(CcuapiException):
    """
    Generic 'catch all' for exceptions related to Akamai
    """
    pass


class AkamaiConfigException(CcuapiException):
    """
    Used to raise exceptions that are specific to the Akamai config.
    This is used with in the context of the configuration file, and isn't
    used for options/run time parameters
    """
    pass


class AkamaiCredentialException(CcuapiException):
    """
    Used when raising issues specific to Credentials
    """
    pass


class AkamaiPurgeTypeException(CcuapiException):
    """
    When an invalid purge type is requested
    """
    pass


class AkamaiAuthenticationException(CcuapiException):
    """
    This exception is raised when a failure to authenticate is encountered.
    It generally indicated a bad username or password
    """
    pass


class AkamaiAuthorizationException(CcuapiException):
    """
    This exception is raised when an authorization exception is encountered.
    It generally means you supplied a valid username and password, however
    you don't have access to whatever you were trying to do.
    """
    pass


class AkamaiArlPurgeWithoutUrls(CcuapiException):
    """
    This is raised when a call has been made to issue a purge, however not urls
    were supplied
    """
    pass


class AkamaiStatusRequestWithoutPurge(CcuapiException):
    """
    This is raised when a user has requested a status of a purge request, but
    has not called the purge method
    """
    pass
