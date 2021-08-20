python3 webserv.py config.cfg &
sleep 1
PID=$!
curl -s -D - -o /dev/null 127.0.0.1:8070/cgibin/3header.py | diff - header_tests/cgi_3_header.out
kill $PID
