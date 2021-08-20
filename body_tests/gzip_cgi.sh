python3 webserv.py example_config.cfg &
sleep 1
PID=$!
curl --output - -sH "Accept-Encoding: gzip" 127.0.0.1:8070/cgibin/paragraph.sh | zdiff - body_tests/gzip_cgi.out.gz
kill $PID
