#! /usr/bin/env sh

echo "#############################"
echo "### Running status tests! ###"
echo "#############################"
count=0
for test in status_tests/*.sh; do
    name=$(basename $test .sh)
    result="$(bash $test)"
    count=$((count+1))
    if $result; then
        echo "$name passed";
    else
        echo "$name failed";
    fi

done

echo "Finished running $count status tests!"
echo

echo "#############################"
echo "### Running header tests! ###"
echo "#############################"
count=0

for test in header_tests/*.sh; do
    name=$(basename $test .sh)
    result="$(bash $test)"
    count=$((count+1))
    if $result; then
        echo "$name passed";
    else
        echo "$name failed";
    fi

done

echo "Finished running $count header tests!"
echo

echo "###########################"
echo "### Running body tests! ###"
echo "###########################"
count=0
for test in body_tests/*.sh; do
    name=$(basename $test .sh)
    result="$(bash $test)"
    count=$((count+1))
    if $result; then
        echo "$name passed";
    else
        echo "$name failed";
    fi

done

echo "Finished running $count body tests!"
echo

echo "####################################"
echo "### Running full response tests! ###"
echo "####################################"
count=0
for test in full_response_tests/*.sh; do
    name=$(basename $test .sh)
    result="$(bash $test)"
    count=$((count+1))
    if $result; then
        echo "$name passed";
    else
        echo "$name failed";
    fi

done


echo "Finished running $count status tests!"
