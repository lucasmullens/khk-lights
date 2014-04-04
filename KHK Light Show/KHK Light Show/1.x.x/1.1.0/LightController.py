# KHK Lighting Controller
# LightController class -- this will create a serial connection to each
# Arduino board, and assign a unique number to each lighting port on the board
#
# Samuel A. Hurley  (C) 4-Nov-2008
# Version 1.0

import serial;

class lightcontroller:

# Map out the number of the light to
# the channel on one of the two Arduino units.

# 0  -> 11 are the frst Arduino channels
# 20 -> 31 are the second Arduino channels
# The index is the 'light number', the value is the arduino channel

  lightArray = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31];

  # Class constructor
  def __init__(self):
    # Open a serial connection to each Arduino
    self.ar1 = serial.Serial(3, 9600);
    self.ar2 = serial.Serial(2, 9600);


  # Method to turn on a light
  # light -> light number
  # timeout -> a timeout value in seconds
  def lightOn(self, light, timeout):
    # Figure out which Arduino and which channel to use
    chan = self.lightArray[light];
    ar = self.ar1;

    if chan > 11:
      chan = chan - 20;
      ar = self.ar2;
    
    # Maximum timeout value is 25.4 seconds
    if timeout > 25.4:
      timeout = 25.4;


    # Granulate the timeout to 0.1 seconds
    timeout = int(round(timeout * 10));

    # Write data to the serial port
    ar.write(chr(255));
    ar.write(chr(chan));
    ar.write(chr(timeout));

  # Method to turn off a light,
  # really just sets lightOn
  def lightOff(self, light):
    self.lightOn(light, 0);

