#!/usr/bin/env python

""" Record a few seconds of audio and plot the fft. """

import pyaudio
import wave
import sys
import random

import LightController 

from scipy import *
#from pylab import *
from time import sleep

chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 22050
RECORD_SECONDS = 1000
WAVE_OUTPUT_FILENAME = "output.wav"


NBINS = 64;
NUMAVE = 22;
TRIGGERLEVEL = 1.2;
TRIGGERBIN = 0;
TRIGGERDWELL = 10;  # Number of cycles to wait before another tigger is possible
bool_BeatLasts = False;

MIN_VOLUME = 6000;


dwell = 0;
p = pyaudio.PyAudio()
lc = LightController.lightcontroller();
all = []
counter1 = 0;
counter2 = 0;

def trigger(counter1):

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
  return counter1;

def turnOnMulti(lights):
  for i in lights:
    lc.lightOn(i, 25.5);

def turnOffMulti(lights):
  for i in lights:
    lc.lightOn(i, 0);


avesamples = zeros(NUMAVE);
a = 0;

print "Opening stream...";
stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = chunk)
print "done.";

while True:
		print("counter1: "+str(counter1))
		stream.start_stream();
		data = stream.read(chunk)
		stream.stop_stream();
		arr = zeros(len(data));
    
		arr = fromstring(data, dtype=short);
		arr = arr;

# Frequency domain:
		arr_fft = abs(fft(arr)[0:129]);
#		plot(abs(fft(arr)[0:128]), '-', [0, 2000000], '-', hold=False);

# Divide into bins
		binwidth = chunk/(2*NBINS);
		bins = zeros(NBINS);

		for i in range(0, NBINS-1):
                  bins[i] = sum(arr_fft[i*binwidth:(1+i)*binwidth]) / binwidth;
		
		#plot(bins[0:10], 'o', [400000, 0], 'o', hold=False, aa=False);
		
# Tally running average
		a = a + 1;
		if a == NUMAVE:
                  a = 0;
			
		avesamples[a] = bins[TRIGGERBIN];
		
# Deincrement the dwell
		dwell = dwell - 1;
		
# Check the bin signal level
                print bins[TRIGGERBIN]
		if bins[TRIGGERBIN] > TRIGGERLEVEL * average(avesamples) and bins[TRIGGERBIN] > MIN_VOLUME:
			if not bool_BeatLasts:					# Only trigger on the start of the beat
				print bins[0];
				# Change the light color
				counter1 = trigger(counter1);
				# Set the dwell counter
				dwell = TRIGGERDWELL;
				bool_BeatLasts = True;
		else:
			bool_BeatLasts = False;

				

