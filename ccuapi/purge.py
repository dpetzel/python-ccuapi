from ccuapi import AKAMAI_USERNAME, AKAMAI_PASSWORD, AKAMAI_NOTIFY_EMAIL, AkamaiException

import urllib, os
from suds.client import Client
from suds.xsd import doctor

QuerySet    =   None
try:
    from django.db.models.query import QuerySet
except:
    pass

class PurgeRequest(object):
    
    def __init__(self, username = AKAMAI_USERNAME, password = AKAMAI_PASSWORD, email = AKAMAI_NOTIFY_EMAIL, options = None, urls = None, wsdl = None, kind = None, domain = None):
        
        self.wsdl   =   wsdl
        self.type   =   kind
        self.domain =   domain
        assert self.type in ['arl', 'cpcode'], "%s is not a valid purge type. Must be arl or cpcode." % self.type
        if not self.wsdl:
            self.wsdl       =   os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ccuapi-axis.wsdl')
            imp             =   doctor.Import('http://schemas.xmlsoap.org/soap/encoding/')
            imp.filter.add('http://www.akamai.com/purge')
            impdoc          =   doctor.ImportDoctor(imp)
            self.client     =   Client("file://%s" % self.wsdl, doctor = impdoc, cache = None)
        self.username   =   username
        if not self.username:
            raise AkamaiException('Username not provided')
        self.password   =   password
        if not self.password:
            raise AkamaiException('Password not provided')
        self.email      =   email
            
        self.options    =   {
            'email-notification-name':  self.email,
            'action':                   'remove',
            'type':                     self.type,
            'domain':                   self.domain,
        }
        if options:
            self.options.update(options)
            
        self.urls   =   []
        if urls is not None:
            self.add(urls)
            
        self.results        =   []
        
    def add(self, urls = None):
        if urls is None:
            raise AkamaiException('urls must be a string, list of strings, Django QuerySet or Django object')
            
        if isinstance(urls, list):
            self.urls.extend(urls)
        elif isinstance(urls, basestring):
            self.urls.append(urls)
        elif QuerySet and isinstance(urls, QuerySet):
            for obj in urls:
                self.add(obj)
        elif hasattr(urls, 'get_absolute_url'):
            self.urls.append(urls.get_absolute_url())
        else:
            raise AkamaiException("Don't know how to handle %r" % urls)
            
    def purge(self):
        self.results    =   []
        self.urls       =   list(set(self.urls)) # removes duplicates
        num_urls        =   len(self.urls)
        while len(self.urls):
            urls            =   self.urls[:100]
            self.urls       =   self.urls[100:]
            if urls:
                self.results.append((self.client.service.purgeRequest(
                    self.username,
                    self.password,
                    '',
                    ["%s=%s" % (k, v) for k, v in self.options.items()],
                    urls
                ), len(urls)))
        return self.results
        
