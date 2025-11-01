from http.server import BaseHTTPRequestHandler, HTTPServer
from jinja2 import Environment, FileSystemLoader
import os
import json
from .write_JSON import write_JSON
from .str_to_datetime import str_to_datetime

jinja_env = Environment(
    loader=FileSystemLoader('pages'),
)
jinja_env.filters['to_datetime'] = str_to_datetime


class HttpServer(BaseHTTPRequestHandler):

    def _set_successful_response(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _set_failed_response(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        error_page = os.path.join("pages", "error.html")
        try:
            with open(error_page, "rb") as f:
                self.wfile.write(f.read())
        except Exception as e:
            print(f"Failed! {e}")

    def _render_template(self, template_name, **kwargs):
        try:
            template = jinja_env.get_template(template_name)
            html = template.render(**kwargs)
            self._set_successful_response()
            self.wfile.write(html.encode('utf-8'))
        except Exception as e:
            print(f"Template error: {e}")
            self._set_failed_response()

    def do_GET(self):

        path = self.path
        if path == '/':
            path = '/index.html'

        if path == '/message.html':
            try:
                with open(os.path.join("storage", "data.json"), "r", encoding='utf-8') as f:
                    messages = json.load(f)
            except Exception as e:
                print(f"Failed to load JSON: {e}")
                messages = {}

            self._render_template('message.html', messages=messages)
            return

        path_name = path.lstrip("/")

        try:
            self._render_template(path_name)
        except:
            self._set_failed_response()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        print(f"Received POST data: {post_data}")

        data_path = os.path.join("storage", "data.json")

        write_JSON(post_data, data_path)

        self.send_response(301)
        self.send_header('Location', 'message.html')
        self.end_headers()
        # self.wfile.write(
        #     f"POST request for {self.path} received. \n Data: {post_data}".encode('utf-8'))


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
