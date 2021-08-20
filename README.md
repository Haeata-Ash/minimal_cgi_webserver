Style: This assignment should follow the style outlined in https://www.python.org/dev/peps/pep-0008/#code-lay-out.

Assumptions:
  I assume that the provided static file path and CGI path is relative, since a server
  would have no need to be aware of anything beyond the scope of its own folder and child folders.

  Similarly I assume that a value provided in the config file, if it exists, will be valid.
  For example, a missing field like exec= is a handled error, but port=not_port is not.

Testing:
  I have separated the tests into full response tests, body tests, header tests and status tests.
  The tests can be run at once with the test_runner.sh file. If there is an error, an errant server
  instance can be killed with the kill_server.sh file.

Extension:
  I chose to implement the gzip extension. I have written tests for gzip and they are distributed
  among the other tests. It is functional for all static files and CGI files.
