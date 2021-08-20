
python3 webserv.py config.cfg &
PID=$!
sleep 1
curl -i 127.0.0.1:8070/ 2> /dev/null | diff - full_response_tests/index_expected.out
kill $PID
