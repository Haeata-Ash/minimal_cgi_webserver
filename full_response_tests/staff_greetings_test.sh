
python3 webserv.py config.cfg &
sleep 1
PID=$!
curl -i 127.0.0.1:8070/greetings.html 2> /dev/null | diff - full_response_tests/greetings_expected.out
kill $PID
