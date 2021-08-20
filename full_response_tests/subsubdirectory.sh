
python3 webserv.py config.cfg &
sleep 1
PID=$!
curl -i 127.0.0.1:8070/files/stowaway/the_depths/mariana_trench.html 2> /dev/null | diff - full_response_tests/subsubdirectory.out
kill $PID
