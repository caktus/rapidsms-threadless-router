import urllib
import copy

from threadless_router.backends.http.outgoing import HttpBackend


class KannelBackend(HttpBackend):

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
