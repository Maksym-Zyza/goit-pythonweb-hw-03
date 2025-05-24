from http.server import HTTPServer, BaseHTTPRequestHandler
import mimetypes
import pathlib
import urllib.parse
from render_messages import render_messages
from save_to_storage import save_to_storage


class SimpleHttpRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == "/":
            self.send_html_file("index.html")
        elif pr_url.path == "/message.html":
            self.send_html_file("message.html")
        elif pr_url.path == "/read":
            render_messages()
            self.send_html_file("messages.html")
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file("error.html", 404)

    def do_POST(self):
      data = self.rfile.read(int(self.headers['Content-Length']))
      data_parse = urllib.parse.unquote_plus(data.decode())
      data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}
      save_to_storage(data_dict)
      self.send_response(302)
      self.send_header('Location', '/')
      self.end_headers()


    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(filename, "rb") as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", "text/plain")
        self.end_headers()
        with open(f".{self.path}", "rb") as file:
            self.wfile.write(file.read())


def run(server_class=HTTPServer, handler_class=SimpleHttpRequestHandler):
    server_address = ("", 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except:
        http.server_close()


if __name__ == "__main__":
    run()
