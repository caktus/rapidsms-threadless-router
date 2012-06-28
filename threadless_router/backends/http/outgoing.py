import urllib
import urllib2

from threadless_router.backends.base import BackendBase


EXAMPLE_URL = 'http://127.0.0.1/'


class HttpBackend(BackendBase):

    def send(self, message):
        self.info('Sending message: %s' % message)
        url = self._config.get('outgoing_url', EXAMPLE_URL)
        data = {'text': message.text,
                'identity': message.connection.identity}
        try:
            self.debug('Opening URL: %s' % url)
            response = urllib2.urlopen(url, urllib.urlencode(data))
        except Exception, e:
            self.exception(e)
            return False
        self.info('SENT')
        self.debug('response: %s' % response.read())
        return True
