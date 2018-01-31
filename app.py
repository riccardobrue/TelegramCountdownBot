# THIS IS THE ENTRY POINT FOR OPENSHIFT

from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from http import HTTPStatus

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Hello, Python!')
        return


def run(server_class=HTTPServer, handler_class=MyHandler):
    server_address = ('telegramcountdownricbot-telegramcountdownricbot.7e14.starter-us-west-2.openshiftapps.com', 8080)
    httpd = server_class(server_address, handler_class)
    try:
        print("Server works on http://localhost:8000")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Stop the server on http://localhost:8000")
        httpd.socket.close()


if __name__ == '__main__':
    run()