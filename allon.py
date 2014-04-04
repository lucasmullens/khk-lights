#/usr/bin/python

from LightController import lightcontroller

NUM_ARDUINOS = 2

lc = lightcontroller()
for i in range(0, 24):
    print i
    lc.lightOff(i)
raw_input('All on.')
for i in range(0, 24):
    lc.lightOff(i)
raw_input('All off.')
raw_input()

