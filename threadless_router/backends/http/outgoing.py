import urllib2

from rapidsms.backends.base import BackendBase


EXAMPLE_URL = 'http://127.0.0.1/?identity=%(identity)s&text=%(text)s'


class HttpBackend(BackendBase):

    def prepare_message(self, message):
        context = {'text': message.text,
                   'identity': message.connection.identity}
        url = self._config.get('outgoing_url', EXAMPLE_URL)
        return url % context

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
        self.debug(response)
        return True
