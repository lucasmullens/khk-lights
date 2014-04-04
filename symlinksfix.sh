#!/bin/sh

rm /dev/ttyS9600
rm /dev/ttyS9601
ln -s /dev/ttyUSB$1 /dev/ttyS9600
ln -s /dev/ttyUSB$2 /dev/ttyS9601
echo "changed to /dev/ttyUSB$1 and /dev/ttyUSB$2"
