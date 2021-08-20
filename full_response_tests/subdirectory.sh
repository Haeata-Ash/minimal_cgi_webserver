
python3 webserv.py config.cfg &
sleep 1
PID=$!
curl -i 127.0.0.1:8070/files/stowaway/sneaky.html 2> /dev/null | diff - full_response_tests/subdirectory.out
kill $PID  
