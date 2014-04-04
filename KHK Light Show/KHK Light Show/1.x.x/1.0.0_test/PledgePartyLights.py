import pyaudio
import wave
import sys

from BeatHandlers import *
import LightController

from scipy import *

# PyAudio Constants
SAMPLE_SIZE = 1024;
FORMAT = pyaudio.paInt16;
CHANNELS = 2;
RATE = 22050;

# Beat Detection Constants
NUM_BANDS = 512;
NUM_AVGS = 22;
TRIGGER_LEVEL = 1.4;		# May be calculated dynamically in final version
TRIGGER_BAND	= 0;	# Will likely be taken out of final version
TRIGGER_CONST_A = -0.0025714;
TRIGGER_CONST_B = 1.5142857;



################################# DetectBeat_Full ##################################
# Author:		Dan Boehm
#
# Description:	From a set of Data, beat detection is performed based on values 
#				stored in a history buffer.
#
# Parameters: 	arr_data - Array of data points in time domain.
#			  	avgSamples - History Buffer
#				pAvgSamples - Pointer to next write location in History Buffer
#
# Modifies:		avgSamples
#
# Returns:		bool_Beat - A boolean representing a detected beat.
#
def DetectBeat_Full(arr_data, avgSamples, pAvgSamples):
	# Calculate instant sound energy
	energy_inst = sum(abs(arr_data));
	
	#Compute Variance
	v = 0;
	
	for a in range(0, NUM_AVGS-1):
		v += avgSamples[a] - average(avgSamples);
	v = v / NUM_AVGS;
	
	#Compute triggerLevel
	triggerLevel = TRIGGER_CONST_A * v + TRIGGER_CONST_B;
		
	# Check for beat
	if energy_inst > TRIGGER_LEVEL * average(avgSamples):
		bool_Beat = True;
	else:
		bool_Beat = False;
		
	# Update History Buffer
	avgSamples[pAvgSamples] = energy_inst
	
	# Return and Exit
	return bool_Beat;
	

	
################################# DetectBeat_FFT ##################################
# Author:		Dan Boehm
#
# Description:	From a set of Data, a FFT is performed.  That data is then
#				separated into frequency bands.  Beat Detection is then performed
#				on each band based on values stored in an array of history buffers.
#
# Parameters: 	arr_data - Array of data points in time domain.
#			  	arr_AvgSamples - Array of History Buffers for each frequency band.
#				pAvgSamples - Pointer to next write location in History Buffer
#
# Modifies:		arr_AvgSamples
#
# Returns:		arr_bool_Beats - An array of booleans representing detected beats
#								 on each frequency band.
#
def DetectBeat_FFT(arr_data, arr_AvgSamples, pAvgSamples):
	arr_bool_Beats = zeros(NUM_BANDS);
	
	# Convert to frequency domain
	arr_fft = abs(fft(arr_data));
	
	# Initialize frequency bands
	bandWidth = SAMPLE_SIZE / (NUM_BANDS);
	bands = zeros(NUM_BANDS);
	
	# Calculate instant sound energy on each band
	for b in range(0, NUM_BANDS-1):
		bands[b] = sum(arr_fft[b*bandWidth:(1+b)*bandWidth]) / bandWidth;
		
	# Check for beats for each frequency band
	for b in range(0, NUM_BANDS-1):
		if bands[b] > TRIGGER_LEVEL * average(arr_AvgSamples[b]):
			arr_bool_Beats[b] = True;
		else:
			arr_bool_Beats[b] = False;

	# Update History Buffer for each frequency band
	for b in range(0, NUM_BANDS-1):
		arr_AvgSamples[b][pAvgSamples] = bands[b];
		
	# Return and Exit
	return arr_bool_Beats;
		


################################## MAIN ######################################

pa = pyaudio.PyAudio();
histBuff = zeros(NUM_AVGS);
histBuff_FFT = zeros([NUM_BANDS, NUM_AVGS]);
pHistBuff = 0;
bool_BeatHistory = False;
bool_BeatHistory_FFT = zeros(NUM_BANDS);
bool_Beat = False;
bool_Beat_FFT = zeros(NUM_BANDS);

lightConfig = 0;
lc = LightController.lightcontroller();

print "Opening stream...";
stream = pa.open(format = FORMAT,
				channels = CHANNELS,
				rate = RATE,
				input = True,
				frames_per_buffer = SAMPLE_SIZE*CHANNELS);
print "Stream opened on default input device."

#Beat Detection
while 1 == 1:
	# Read sample into array
	stream.start_stream();
	data = stream.read(SAMPLE_SIZE);	# When multiple channels are
	stream.stop_stream();					# streamed, the audio is
											# interleaved.
	arr_raw = zeros(len(data));
	arr_raw = fromstring(data, dtype=short);
	
	# De-interleave and Sum each channel to yield a mono wave.
	arr_ChanData = zeros([SAMPLE_SIZE, CHANNELS]);
	for i in range(0, len(arr_raw)-1):
		arr_ChanData[i/CHANNELS][i%CHANNELS] = arr_raw[i];
	
	arr_Summed = zeros(SAMPLE_SIZE);
	for i in range(0, SAMPLE_SIZE-1):
		arr_Summed[i] = sum(arr_ChanData[i]);
	
	# Execute Beat Detection
	bool_Beat_FFT = DetectBeat_FFT(arr_Summed, histBuff_FFT, pHistBuff);
	#bool_Beat = DetectBeat_Full(arr_Summed, histBuff, pHistBuff);
	
	if bool_Beat_FFT[TRIGGER_BAND]:# and bool_Beat:
		if not bool_BeatHistory_FFT[TRIGGER_BAND]:# or bool_BeatHistory):
			bool_BeatHistory_FFT[TRIGGER_BAND] = True;
			bool_BeatHistory = True;
			ChangeLights(lightConfig, lc);
			lightConfig = lightConfig + 1;
			print "beat detected - {}" .format(pHistBuff);
	else:
		bool_BeatHistory_FFT[TRIGGER_BAND] = False;
		bool_BeatHistory = False;
	
	# Update History Buffer Pointer
	pHistBuff = pHistBuff + 1;
	if pHistBuff == NUM_AVGS:
		pHistBuff = 0;
