from LightController import *

lc = lightcontroller()

print "Welcome to Light Tester"
print ""
raw_input("Press Enter to begin...")

for i in range(12):
    print "{} - ON" .format(i)
    lc.lightOn(i, 1)
    #raw_input()
    #lc.lightOff(i)

for i in range(13, 24):
    print "{} - ON" .format(i)
    lc.lightOn(i, 1)
    #raw_input()
    #lc.lightOff(i)

raw_input("Press Enter to begin...")
for i in range(12):
    print "{} - off" .format(i)
    lc.lightOff(i)
    #raw_input()
    #lc.lightOff(i)
    
for i in range(20, 32):
    print "{} - ON" .format(i)
    lc.lightOff(i, 1)
    #raw_input()
    #lc.lightOff(i)
    
raw_input("Press Enter When Finished")
