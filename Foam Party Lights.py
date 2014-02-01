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
  print counter1

  if counter1 == 0:
    turnOffMulti([9,5,15,7]);
    turnOnMulti([8,9,5,7,13]);

  if counter1 == 1:
    turnOffMulti([8,9,5,7,13]);
    turnOnMulti([16,9,15,18]);

  if counter1 == 2:
    turnOffMulti([16,9,15,18]);
    turnOnMulti([13,18,16,5]);

  if counter1 == 3:
    turnOffMulti([13,18,16,5]);
    turnOnMulti([5,8,13,7]);

  if counter1 == 4:
    turnOffMulti([5,8,13,7]);
    turnOnMulti([16,8,5,7,15]);

  if counter1 == 5:
    turnOffMulti([16,8,5,7,15]);
    turnOnMulti([9,5,15,7]);

  if counter1 == 6:
    turnOffMulti([9,5,15,7]);
    turnOnMulti([5,7,8,9,13,15,16,18]);

  if counter1 == 7:
    turnOffMulti([5,7,8,9,13,15,16,18]);
    turnOnMulti([9,5,15,7]);

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
				

