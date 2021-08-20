# Minimal CGI Webserver

This webserver implements a subset of  ![Common Gateway Interface](https://tools.ietf.org/html/rfc3875) specification and HTTP methods (only GET requests). 

The webserver respects the following request headers:
- `Accept`
- `Host`
- `User-Agent`
- `Accept-Encoding`
- `Remote-Address`
- `Content-Type`
- `Content-Length`

Accepted content-types:
- `text/plain`
- `text/html`
- `application/javascript`
- `text/css`
- `image/png`
- `image/jpeg`
- `text/xml`

The webserver is capable of sending an accepting gzip encoded packets.

## Configuration
A path to a configuration file must be passed as an argument when starting the webserver. The configuration file is a simple text file. An example configuration file is provided.

Four properties must be set in the config file:
- staticfiles: a **relative** path to static files
- cgibin: **relative** path to cgi executables
- port: port to listen on
- exec: string, executable path or command that will be executed on inbound cgibin requests

Style: This assignment follows the style outlined in https://www.python.org/dev/peps/pep-0008/#code-lay-out.

## Testing
I have separated the tests into full response tests, body tests, header tests and status tests. The tests can be run at once with the test\_runner.sh file. If there is an error, an errant server
  instance can be killed with the kill\_server.sh file.

Style: This assignment follows the style outlined in https://www.python.org/dev/peps/pep-0008/#code-lay-out.
