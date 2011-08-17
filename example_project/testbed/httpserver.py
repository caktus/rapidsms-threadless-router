import urllib
import urlparse
import BaseHTTPServer
from optparse import OptionParser


parser = OptionParser()
parser.add_option("-p", "--port", dest="port", default=9898)
parser.add_option("-a", "--address", dest="address", default='')
parser.add_option("-r", "--rapidsms", dest="rapidsms", default='')


class AcceptHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):
        parser = urlparse.urlparse(self.path)
        if parser.path == '/out/':
            print 'Outbound message to phone network: {0}'.format(parser.query)
            self.send_response(200)
        elif parser.path == '/rapidsms/' and self.server.options.rapidsms:
            print 'Inbound message to RapidSMS: {0}'.format(parser.query)
            url = self.server.options.rapidsms
            f = urllib.urlopen("{url}?{query}".format(url=url,
                                                      query=parser.query))
            print "Response: {0}".format(f.read())
            self.send_response(200)
        else:
            self.send_response(404)

    def do_POST(self):
        self.send_response(200)


def run(options):
    address = (options.address, options.port)
    httpd = BaseHTTPServer.HTTPServer(address, AcceptHandler)
    httpd.options = options
    pretty_address = options.address or 'localhost'
    print "HTTP server running at http://{0}:{1}/".format(pretty_address,
                                                          options.port)
    httpd.serve_forever()


if __name__ == "__main__":
    (options, args) = parser.parse_args()
    run(options)
