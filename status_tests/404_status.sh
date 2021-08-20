python3 webserv.py config.cfg &
sleep 1
PID=$!
curl -I 127.0.0.1:8070/missing.html 2> /dev/null | grep '404' | diff - status_tests/404_status_expected.out
kill $PID
