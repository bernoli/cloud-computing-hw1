#!/bin/bash
 
response=$(redis-cli ping)
pong="PONG"
ready=0
while [ $ready -le 9 ]
do
	if  [ "$response" != "$pong" ]; then
	    echo "redis is not ready trying again."
        ready=$(($ready+1))
        echo "$ready out of 10"
        sleep $ready
        response=$(redis-cli ping)
	else
	    echo "redis is ready - $response"
        ready=100
	fi
done
