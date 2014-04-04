from LightController import *

lc = lightcontroller()

print "Welcome to Light Tester"
print ""
raw_input("Press Enter to begin...")

for i in range(12):
    print "{} - ON" .format(i)
    lc.lightOn(i, 1)
    raw_input()
    lc.lightOff(i)
