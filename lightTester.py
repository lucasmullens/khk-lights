#/usr/bin/python

from LightController import lightcontroller

NUM_ARDUINOS = 2

lc = lightcontroller()

for i in range(0,12):
    lc.lightOn(i, 1)
    
    raw_input('channel {} is on... [Press Enter]'.format(i))
    
    lc.lightOff(i)

#lc.lightOn(0, 1)
#lc.lightOff(0)
    
if NUM_ARDUINOS is 2:
    for i in range(12, 24):
        lc.lightOn(i, 1)
        
        raw_input('channel {} is on... [Press Enter]'.format(i))
    
        lc.lightOff(i)

raw_input()

