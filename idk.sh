#!/bin/sh
rm /dev/ttyS9600
rm /dev/ttyS9601
ln -s /dev/ttyUSB2 /dev/ttyS9600
ln -s /dev/ttyUSB3 /dev/ttyS9601
