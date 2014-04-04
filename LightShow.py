#!/usr/bin/env python

""" Record a few seconds of audio and plot the fft. """

# import pyaudio
# import wave
import sys
import random

import LightController 

from scipy import *
#from pylab import *
from time import sleep

chunk = 1024
# FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 2050
RECORD_SECONDS = 1000
WAVE_OUTPUT_FILENAME = "output.wav"


NBINS = 64;
NUMAVE = 12;
TRIGGERLEVEL = 1.2;
TRIGGERBIN = 0;
TRIGGERDWELL = 10;  # Number of cycles to wait before another tigger is possible


dwell = 0;
# p = pyaudio.PyAudio()
lc = LightController.lightcontroller();
all = []
counter1 = 0;
counter2 = 0;

def trigger(counter1):
# Today's scheme: RGB
  print counter1

  if counter1 == 0:
    turnOffMulti([16,18,6]);
    turnOnMulti([3,6,11,0,7,12,4]);

  if counter1 == 1:
    turnOffMulti([3,6,11,0,7,12,4]);
    turnOnMulti([16,18,5,15,22,9]);

  if counter1 == 2:
    turnOffMulti([16,18,5,15,22,9]);
    turnOnMulti([11,18,6,16,0,5,7,12,15,22,4,9,14]);

  if counter1 == 3:
    turnOffMulti([11,18,6,16,0,5,7,12,15,22,4,9,14]);
    turnOnMulti([3,6,18,0,5,7,12,15,22,4,9,14]);

  if counter1 == 4:
    turnOffMulti([3,6,18,0,5,7,12,15,22,4,9,14]);
    turnOnMulti([3,11,16,7,5,15,4,9]);

  if counter1 == 5:
    turnOffMulti([3,11,16,7,5,15,4,9]);
    turnOnMulti([6,18,7,22,12,14,9]);

  if counter1 == 6:
    turnOffMulti([6,18,7,22,12,14,9]);
    turnOnMulti([3,16,11,0,22,14]);

  if counter1 == 7:
    turnOffMulti([3,16,11,0,22,14]);
    turnOnMulti([3,18,6]);

  counter1 = counter1 + 1;
  if counter1 == 8:
    counter1 = 0;

# Today's scheme, turn on 5 random lights at each beat
#  for i in range(1,5):
#    lc.lightOn(random.randint(0,23), .75);

  return counter1;

def turnOnMulti(lights):
  for i in lights:
    lc.lightOn(i, 1);

def turnOffMulti(lights):
  for i in lights:
    lc.lightOn(i, 0);


avesamples = zeros(NUMAVE);
a = 0;

print 'Running light controller...';
print 'To stop lights, close this window.';


while 1 == 1:
  sleep(.8);
  # Change the light color
  counter1 = trigger(counter1);
  # Set the dwell counter
  dwell = TRIGGERDWELL;
				

