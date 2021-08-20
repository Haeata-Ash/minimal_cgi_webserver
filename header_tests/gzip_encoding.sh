
python3 webserv.py config.cfg &
sleep 1
PID=$!
curl --output - -sIH "Accept-Encoding: gzip" 127.0.0.1:8070/files/greetings.html | diff - header_tests/gzip_encoding.out 
kill $PID