

class HTTPRequest:
    """Class representing a HTTP requests. Responsible for parsing raw requests as
    well as seperating and storing the relevant fields"""

    #valid content_types of server
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

    def __init__(self, raw_request):
        """Takes a request string and parses it, storing all relevant fields"""
        self.raw_request = raw_request
        self.version = "1.1"
        self.method = None
        self.url = None
        self.path = None
        self.headers = {}
        self.content_type = None
        self.body = None
        self.query = None
        self.parse_request(raw_request)

    def parse_request(self, request):
        """Parse the request and set attributes"""
        request = request.split(b"\r\n\r\n") #split into protocol/headers and body
        protocol_and_headers = request[0].split(b"\r\n") # split protocol and headers

        # get body
        if len(request) < 2:
            if request[1]:
                self.body = request[1].decode()


        # get method, url, version, path, content type and any queries
        request_protocol = protocol_and_headers[0].split(b" ")
        self.method = request_protocol[0].decode()
        self.url = request_protocol[1].decode()
        self.path = self.get_path()
        self.content_type = self.get_content_type()
        self.query = self.get_query()

        # get headers
        self.get_headers(protocol_and_headers[1:])

    def get_headers(self, header_lines):
        """Create dictionary of headers"""
        for ln in header_lines:
            ln = ln.split(b": ", 1)
            self.headers[ln[0].decode()] = ln[1].decode()

    def get_header(self, key):
        """Gets a specifc header"""
        if key in self.headers:
            return self.headers[key]
        else:
            None

    def get_path(self):
        """Get the path"""
        path = self.url.split("?", 1)[0].strip("/")
        path = path.split("/", 1)[-1]
        return path

    def get_content_type(self):
        """Get the content type"""
        try:
            file_type = "." + self.path.split(".")[1]
            content_type = self.CONTENT_TYPE_MAP[file_type]

        # not a valid content  type
        except (KeyError, IndexError):
            return None
        return content_type


    def get_query(self, asDict=False):
        """Parse the query and optionally create dictionary of query keys and values"""

        url_components = self.url.split("?", 1)

        # no query
        if len(url_components) < 2:
            if asDict:
                return {}
            else:
                return ""

        # query exists
        else:
            url_query = url_components[1]
            if not asDict:
                return url_query

        key_value_pairs = url_query.split("&")
        query_dict = {}

        # create dictionary
        for k_v in key_value_pairs:
            k_v = k_v.split("=")
            query_dict[k_v[0]] = k_v[1]

        return query_dict
