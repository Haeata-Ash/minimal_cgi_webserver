python3 webserv.py config.cfg &
sleep 1
PID=$!
curl --output - -sH "Accept-Encoding: gzip" 127.0.0.1:8070/files/PNG.png | zdiff - body_tests/PNG.png.gz
kill $PID