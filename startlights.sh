#!/bin/sh

#fix the issue with the USB's randomly being different numbers
rm -rf /dev/ttyS9600
rm -rf /dev/ttyS9601
for i in $(seq 0 10);
    do
    	FILE="/dev/ttyUSB$i"

    	if [ -c $FILE ];
    	then
    		j=$((i+1));
    		echo $j;
			ln -s /dev/ttyUSB$i /dev/ttyS9600
			ln -s /dev/ttyUSB$j /dev/ttyS9601
			break;
    	fi
    done

#start the lights
python /home/khk/Desktop/khk-lights/startlights.py