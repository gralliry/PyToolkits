import base64
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import urllib.parse

USERNAME = "user"
PASSWORD = "password"


class HttpRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, username, password, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = username
        self.password = password

    def do_GET(self):
        if not self.is_authenticated():
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Login Required"')
            self.end_headers()
            self.wfile.write(b'Authentication required.')
            return

        # 解析请求路径
        parsed_url = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_url.query)

        # 获取参数 'path'
        file_path = query_params.get('path', [None])[0]

        # 处理 'path' 参数
        if not isinstance(file_path, str):
            # 如果没有提供 'path' 参数，返回 400 错误
            self.send_error(400, "Bad Request: 'path' parameter is required")
            return

        file_path = file_path.strip('"\'').replace("\\\\", "/").replace("\\", "/")

        if not os.path.isfile(file_path):
            # 如果文件不存在，返回 404 错误
            self.send_error(404, "File not found")
            return

        # 如果文件存在，返回文件内容
        self.send_response(200)
        self.send_header("Content-type", "application/octet-stream")
        self.send_header("Content-Disposition", f"attachment; filename={os.path.basename(file_path)}")
        self.end_headers()

        with open(file_path, 'rb') as file:
            self.wfile.write(file.read())

        return

    def is_authenticated(self):
        """检查请求是否经过身份验证"""
        if 'Authorization' not in self.headers:
            return False

        auth_header = self.headers['Authorization']
        if not auth_header.startswith('Basic '):
            return False

        # 解码 Base64 编码的凭据
        encoded_credentials = auth_header[len('Basic '):]
        decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        username, password = decoded_credentials.split(':', 1)

        return username == USERNAME and password == PASSWORD


def create_server(port, username, password, ip="0.0.0.0", verbose=True):
    global USERNAME, PASSWORD
    USERNAME = username
    PASSWORD = password
    if verbose:
        print(f"Serving files at http://127.0.0.1:{port}")
    # 创建并启动服务器
    httpd = HTTPServer((ip, port), HttpRequestHandler)
    httpd.serve_forever()
