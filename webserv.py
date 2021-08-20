import sys, socket, os, re, threading, gzip
from config import parse_config, get_config
from HTTPRequest import HTTPRequest


class Server:
    """Base server class. Manages connections and holds config fields
    specified in configuration file"""

    def __init__(self, port, staticfiles, cgibin, exec):
        """Assigns config values, address and packet size"""
        self.port = int(port)
        self.staticfile_path = staticfiles
        self.cgibin_path = cgibin
        self.exec_path = exec.strip()
        self.host = "127.0.0.1"
        self.packet_size = 1024

    def start(self):
        """Starts the server"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)

        while True:
            (c_socket, address) = server_socket.accept()

            # conncurrent connections get a new thread
            if c_socket:
                conn_thread = threading.Thread(target=self.handle_client, args=(c_socket, address))
                conn_thread.start()

    def handle_request(self, data):
        """Method to be overwritten by child classes"""
        return data

    def handle_client(self, c_socket, address):
        """Sends response back to client"""

        request = c_socket.recv(self.packet_size)
        response = self.handle_request(request, address)
        c_socket.sendall(response)
        c_socket.close()



class HTTPServer(Server):
    """Builds on base server to handle and fulfill http requests"""

    CONTENT_TYPE_MAP = {
        ".txt": "text/plain",
        ".html": "text/html",
        ".js": "application/javascript",
        ".css": "text/css",
        ".png": "image/png",
        ".jpeg": "image/jepg",
        ".jpg": "image/jpeg",
        ".xml": "text/xml"
    }

    STATUS_CODES = {
        200: "OK",
        404: "File not found",
        500: "Internal Server Error",
        501: "Not Implemented"
    }

    def handle_request(self, data, address):
        """Handles requests. Splits into cgi or static request"""

        request = HTTPRequest(data)
        path = request.get_path()

        #index
        if not path:
            path = f"{self.staticfile_path}/index.html"
            request.content_type = "text/html"
            response = self.static_file_handler(request, path)

        #static
        elif os.path.exists(self.staticfile_path + "/" + path) and not os.path.isdir(self.staticfile_path + "/" + path):
            response = self.static_file_handler(request, self.staticfile_path + "/" + path)

        #cgi
        elif os.path.exists(self.cgibin_path + "/" + path) and not os.path.isdir(self.cgibin_path + "/" + path):
            response = self.cgi_handler(request, self.cgibin_path + "/" + path, address)

        #not a valid path to resource
        else:
            response = self.send_error(404)

        return response

    def get_static_file(self, path, compress):
        """Retrieves a file"""

        #gzip
        if compress:
            with open(path, "rb") as file:
                contents = file.read()
                contents = gzip.compress(contents)

        #normal
        else:
            with open(path, "rb") as file:
                contents = file.read()

        return contents

    def static_file_handler(self, request, path):
        """Handles static requests"""

        response_headers = {}
        compress = False

        #sets content_type header
        content_type = request.content_type
        response_headers["Content-Type"] = content_type
        if not content_type:
            return self.send_error(404)

        # checks if compression is accepted
        if "Accept-Encoding" in request.headers:
            if "gzip" in request.headers["Accept-Encoding"]:
                compress = True
                # adds encoding header
                response_headers["Content-Encoding"] = "gzip"

        try:
            body = self.get_static_file(path, compress)
        except OSError:
            return self.send_error(501)

        # create headers and status
        status_string = self.build_status_string(200)
        headers = self.build_response_header_string(response_headers)

        #build response
        response = self.make_response(status_string, headers, body)

        return response

    def build_response_header_string(self, headers):
        """Creates header string for dictionary"""
        header_list = []

        #no response headers
        if not headers:
            return str.encode("")

        # turns header dictionary into string
        else:
            for k, v in headers.items():
                header_list.append(f"{k}: {v}")
            headers_string = "\n".join(header_list) + "\n"
            return str.encode(headers_string)

    def build_status_string(self, status_code, custom_message=None):
        """Create status line"""

        if not custom_message:
            status_string = f"HTTP/1.1 {status_code} {self.STATUS_CODES[status_code]}\n"
        else:
            status_string = f"HTTP/1.1 {status_code} {custom_message}\n"
        return str.encode(status_string)

    def populate_environ(self, request, address):
        """Creates environment variables for cgibin"""

        cgi_env_vars = {
            "HTTP_ACCEPT": None,
            "HTTP_HOST": None,
            "HTTP_USER_AGENT": None,
            "HTTP_ACCEPT_ENCODING": None,
            "REQUEST_METHOD": None,
            "REMOTE_ADDRESS": None,
            "REMOTE_PORT": None,
            "REQUEST_URl": None,
            "SERVER_ADDR": None,
            "SERVER_PORT": None,
            "CONTENT_TYPE": None,
            "CONTENT_LENGTH": None,
            "QUERY_STRING": None
        }

        cgi_env_vars["HTTP_ACCEPT"] = request.get_header("Accept")
        cgi_env_vars["HTTP_HOST"] = request.get_header("Host")
        cgi_env_vars["HTTP_USER_AGENT"] = request.get_header("User-Agent")
        cgi_env_vars["HTTP_ACCEPT_ENCODING"] = request.get_header("Accept-Encoding")
        cgi_env_vars["QUERY_STRING"] = request.query
        cgi_env_vars["REQUEST_METHOD"] = request.method
        cgi_env_vars["REQUEST_URI"] = request.url

        cgi_env_vars["REMOTE_PORT"] = str(address[1])
        cgi_env_vars["REMOTE_ADDRESS"] = address[0]

        cgi_env_vars["SERVER_ADDR"] = self.host
        cgi_env_vars["SERVER_PORT"] = str(self.port)

        for k,v in cgi_env_vars.items():
            if v:
                os.environ[k] = v

        return os.environ

    def make_response(self, status_string, headers_string, body_string):
        """Formats the status line, headers and body"""

        if not body_string:
            response_string = status_string + headers_string
        elif not body_string and not headers_string:
            response_string = status_string
        else:
            response_string = status_string + headers_string + b"\n" + body_string
        return response_string

    def send_error(self, status_code):
        """Creates error response for code"""

        stat_str = self.build_status_string(status_code)
        header_str = self.build_response_header_string({"content-type": "text/html"})
        path = f"{self.staticfile_path}/{status_code}.html"
        body = self.get_static_file(path, False)

        return self.make_response(stat_str, header_str, body)


    def cgi_handler(self, request, path, address):
        """Handles cgi requests"""

        #sets environ vars
        environ = self.populate_environ(request, address)

        try:
            r, w = os.pipe()
            pid = os.fork()

            #child
            if pid == 0:
                os.close(r)
                os.dup2(w, 1)
                os.dup2(w, 2)
                os.execve(self.exec_path, [self.exec_path, path], environ)

            #parent
            elif pid > 0:
                os.close(w)
                ret_val = os.wait()

                #read in output
                if ret_val[1] == 0:
                    r = os.fdopen(r)
                    content = r.read()


                # error in child
                else:
                    return self.send_error(500)
            # error in fork
            else:
                return self.send_error(500)

        # Unspecified error
        except OSError:
            return self.send_error(500)

        # scoop headers/status string from cgi output
        body, headers, status_string = self.get_cgi_headers(content)

        if not status_string:
            status_string = self.build_status_string(200)
        header_string = self.build_response_header_string(headers)
        body = str.encode(body)

        #compression
        compress = False
        if "Accept-Encoding" in request.headers:
            if "gzip" in request.headers["Accept-Encoding"]:
                compress = True
                header_string += str.encode("Content-Encoding: gzip\n")

        if compress:
            body = gzip.compress(body)

        return self.make_response(status_string, header_string, body)

    def get_cgi_headers(self, body):
        """Looks for headers or custom status in cgi output"""

        if body:
            lines = body.split("\n")

        #matches headers
        header_re = re.compile("(?P<key>([\S]+)): (?P<value>([\S]+))")
        headers = {}

        #matches status
        status_string = None
        custom_status_re = re.compile("Status-Code: (?P<code>([\d]{3})) (?P<msg>(.+))")

        i = 0
        if lines:
            while i < len(lines):
                #check for header or status in line
                header = header_re.match(lines[i])
                status = custom_status_re.match(lines[i])

                if status:
                    status_string = self.build_status_string(status.group("code"), status.group("msg"))

                elif header:
                    headers[header.group("key")] = header.group("value")

                # if no header or status break as reached body
                else:
                    break

                i += 1

        # remove any header/status lines
        if i > 0:
            lines = lines[i+1:]

        return "\n".join(lines), headers, status_string


if __name__ == '__main__':
        config = get_config()
        s = HTTPServer(**config)
        s.start()
