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
RATE = 22050
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
  turnOffMulti([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]);
  l = []
  for i in range(0,24):
    j = random.randint(0,3)
    if j == 0:
      l.append(i)
      print i
  turnOnMulti(l);


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
				

