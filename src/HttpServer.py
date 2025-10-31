from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape

jinja_env = Environment(
    loader=FileSystemLoader(os.path.join(
        os.path.dirname(__file__), '..', 'pages')),
    autoescape=select_autoescape(['html'])
)

messages = [
    "Привіт!",
    "Це тестове повідомлення",
    "Jinja2 працює!"
]


class HttpServer(BaseHTTPRequestHandler):

    def _set_successful_response(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _set_failed_response(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        try:
            template = jinja_env.get_template('error.html')
            self.wfile.write(template.render().encode('utf-8'))
        except:
            self.wfile.write(b'404 - Not Found')

    def _render_template(self, template_name, **kwargs):
        try:
            template = jinja_env.get_template(template_name)
            self._set_successful_response()
            self.wfile.write(template.render(**kwargs).encode('utf-8'))
        except Exception as e:
            print(f"Template error: {e}")
            self._set_failed_response()

    def do_GET(self):
        try:
            if self.path=='/':
                self.path='/index.html'
            self._render_template(self.path[1:], messages=messages)
        except:
            self._set_failed_response()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        print(f"Received POST data: {post_data}")

        messages.append(post_data)

        self._set_successful_response()
        self.wfile.write(
            f"POST request for {self.path} received".encode('utf-8'))


def run(server_class=HTTPServer, handler_class=HttpServer, port=3000):
    print(f"Starting server on port {port}")
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Stop the server")
    httpd.server_close()


if __name__ == "__main__":
    run()
