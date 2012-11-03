import os,sys,ConfigParser

django_settings =   False
try:
    from django.conf import settings as django_settings
except ImportError:
    pass

class AkamaiException(Exception):
    pass
    
class AkamaiConfigException(Exception):
    pass

AKAMAI_USERNAME     =   os.environ.get('AKAMAI_USERNAME', None)
AKAMAI_PASSWORD     =   os.environ.get('AKAMAI_PASSWORD', None)
AKAMAI_NOTIFY_EMAIL =   os.environ.get('AKAMAI_NOTIFY_EMAIL', None)

if django_settings:
    try:
        AKAMAI_USERNAME     =   getattr(django_settings, 'AKAMAI_USERNAME', AKAMAI_USERNAME)
        AKAMAI_PASSWORD     =   getattr(django_settings, 'AKAMAI_PASSWORD', AKAMAI_PASSWORD)
        AKAMAI_NOTIFY_EMAIL =   getattr(django_settings, 'AKAMAI_NOTIFY_EMAIL', AKAMAI_NOTIFY_EMAIL)
    except ImportError:
        pass # this isn't being run inside a Django environment


if not AKAMAI_USERNAME or not AKAMAI_PASSWORD:
    config  =   ConfigParser.SafeConfigParser()
    config.readfp(open(os.path.expanduser('~/.akamai')))
    if os.path.exists(os.path.expanduser('~/.akamai')):
        if config.has_section('Credentials'):
            if config.has_option('Credentials', 'username'):
                AKAMAI_USERNAME =   config.get('Credentials', 'username')
            else:
                raise AkamaiConfigException('.akamai config is missing username')
            if config.has_option('Credentials', 'password'):
                AKAMAI_PASSWORD =   config.get('Credentials', 'password')
            else:
                raise AkamaiConfigException('.akamai config is missing username')
        else:
            raise AkamaiConfigException('.akamai config is missing the Credentials section')
    else:
        raise AkamaiConfigException('Akamai credentials were not found in either enivronment variables or in a .akamai config file')
        
if not AKAMAI_NOTIFY_EMAIL and config.has_section('Notifications') and config.has_option('Notifications', 'email'):
    AKAMAI_NOTIFY_EMAIL =   config.get('Notifications', 'email')

from . import purge
__all__ =   ['purge',]
