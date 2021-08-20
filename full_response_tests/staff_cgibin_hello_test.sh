python3 webserv.py config.cfg &
sleep 1
PID=$!
curl -i 127.0.0.1:8070/cgibin/hello.py 2> /dev/null | diff - full_response_tests/cgi_hello.out
kill $PID
