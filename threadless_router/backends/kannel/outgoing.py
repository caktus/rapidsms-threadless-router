import urllib
import urllib2
import copy

from threadless_router.backends.base import BackendBase


class KannelBackend(BackendBase):

    def configure(self, sendsms_url='http://127.0.0.1:13013/cgi-bin/sendsms',
                  sendsms_params=None, charset=None, coding=None,
                  encode_errors=None, **kwargs):
        self.sendsms_url = sendsms_url
        self.sendsms_params = sendsms_params or {}
        self.charset = charset or 'ascii'
        self.coding = coding or 0
        self.encode_errors = encode_errors or 'ignore'

    def prepare_message(self, message):
        url_args = copy.copy(self.sendsms_params)
        url_args['to'] = message.connection.identity
        url_args['text'] = message.text.encode(self.charset,
                                               self.encode_errors)
        url_args['coding'] = self.coding
        url_args['charset'] = self.charset
        url = '?'.join([self.sendsms_url, urllib.urlencode(url_args)])
        return url

    def send(self, message):
        self.info('Sending message: %s' % message)
        url = self.prepare_message(message)
        try:
            self.debug('Opening URL: %s' % url)
            response = urllib2.urlopen(url)
        except Exception, e:
            self.exception(e)
            return False
        self.info('SENT')
        self.debug('response: %s' % response.read())
        return True
