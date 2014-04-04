import serial

ar = serial.Serial()
ar.port     = 2
ar.baudrate = 9600
bytesWritten = 0

ar.open()
i = 0

raw_input("press enter")

while(True):
    bytesWritten = bytesWritten + ar.write(chr(255))
    bytesWritten = bytesWritten + ar.write(chr(i))
    bytesWritten = bytesWritten + ar.write(chr(1))

    #print bytesWritten

    raw_input("press enter")
    bytesWritten = bytesWritten + ar.write(chr(255))
    bytesWritten = bytesWritten + ar.write(chr(i))
    bytesWritten = bytesWritten + ar.write(chr(0)) 
    i = i+1
