python3 webserv.py config.cfg &
sleep 1
PID=$!
curl -I 127.0.0.1:8070/ 2> /dev/null | grep '200 OK' | diff - status_tests/index_status.out
kill $PID
