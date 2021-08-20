python3 webserv.py config.cfg &
sleep 1
PID=$!
curl -o - 127.0.0.1:8070/files/image.jpg 2> /dev/null | diff - body_tests/jpeg.out
kill $PID
