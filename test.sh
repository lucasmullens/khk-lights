#!/bin/sh
for i in $(seq 0 10);
    do
    	FILE="/dev/ttyUSB$i"

    	if [ -c $FILE ];
    	then
    	   echo "File $FILE exists.";
		   TEST="/dev/ttyS9600";
    	   break;
    	fi
        echo $i
    done