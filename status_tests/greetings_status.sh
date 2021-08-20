python3 webserv.py config.cfg &
sleep 1
PID=$!
curl -I 127.0.0.1:8070/files/greetings.html 2> /dev/null | grep '200 OK' | diff - status_tests/greetings_status_expected.out
kill $PID
