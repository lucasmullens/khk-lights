######################################### KHK Light Show ###########################################
# Author:			Dan Boehm
#
# Version:			2.0.0
#
# Description:		KHK Light Show is an application for use with the Dance Light 
#					Control Hardware in the basement as it was installed by
#					Dan Boehm in May 2011.  KHK Light Show samples the audio input 
#					from the default recording device on a Windows Computer.  The 
#					software then performs beat detection and other music analysis
#					algorithms on that audio signal.  Based on this analysis, 
#					KHK Light Show controls the Dance Lights.
#				
#					This version of the software assumes a bang-bang implementation 
#					of the Dance Lights (ie: either on or off).  Future versions of 
#					this software may include support for the use of DMX busses for 
#					the control of more advanced lighting.
#
#					For more info on system requirements, hardware setup, and 
#					enabling or disabling certain software features, along with 
#					terms of use and other legal info, please refer to the readme
#					packaged with this software.
#
# Included Modules:	BeatDetector
#					LightSelector
#
# Copyright:		2011
#
# Developed for:	Python 2.7.1
#
# 3rd Party Modules:	pyAudio
# 						scipy
#
####################################################################################################

############################################ MODULES ###############################################
import string
import sys
import pyaudio

from scipy import zeros
from numpy import fft



########################################### CONSTANTS ##############################################
STR_ERROR = {	'configDNE' : "config.ini invalid or missing.  Using default values...",
				'error' : "ERROR: " }
STR_INIT = {	'pa_Opening' : "Opening Stream...",
				'pa_Opened' : "Stream opened on audio input device.",
				'pa_ID' : "\t Device ID: {})",
				'pa_Channels' : "\t Channels: {}",
				'pa_SampRate' : "\t Sample Rate: {}",
				'pa_SampSize' : "\t Sample Size: {}" }
PYAUDIO_FORMAT = pyaudio.paInt16

########################################## GLOBAL VARS #############################################

##### Command Line #####
config_Loc = config.ini


##### Config #####
# pyaudio
deviceID = 0
sampleSize = 1024
NumChannels = 1
sampleRate = 22050

# beatDetection
useFreqBands = False
numFreqBands = 10
ignoreHighBand = True
freqRangePercentage = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
useDynamicTrigger = False
linRegConst_A = -0.0025714
linRegConst_B = 1.5142857
triggerConst_Main = 1.5
triggerConst_Bands = [1.5, 1.5, 1.5, 1.5, 1.5]
useDynamicHistBuffer = False
histBufferSize = 22

# lightController
comA = 3
baudA = 9600
comB = 2
baudB = 9600

######################################### STATIC METHODS ###########################################

###################### analyzeMusicFrame ########################
#
# Description:	Takes info from beatDetectors and processes it to create a MusicFrameData Object
#				for use in light control.
#
# Parameters: 	beatDetectors - An array of BeatDetector objects that have just processed the 
#								frame of Music being analyzed.
#
# Modifies:		none
#
# Returns:		A MusicFrameData object created from the data in beatDetectors.
#	
def analyzeMusicFrame(beatDetectors):
	numBands = len(beatDetectors) - 1
	useBands = numBands == 0
	
	# Find the initial beat ratio.
	beat_Main = beatDetectors[0].energyLevel / beatDetectors[0].triggerConstant
	
	if(useBands):
		for i in range(numBands):
			beat_Bands[i] = beatDetectors[i+1].energyLevel / beatDetectors[i+1].triggerConstant
	
	# Determine if Beat should be Ignored.
	# Beats are ignored for the following reasons: 
	#	- Beat previously, but never dropped below trigger again
	#
	if(beatDetectors[0].beatDetected):
		if(beatDetectors[0].getBeatHistory()[1]):
			beat_Main = -beat_Main
	
	for i in range(numBands):
		if(beatDetectors[i+1].beatDetected):
			if(beatDetectors[0].getBeatHistory()[1]):
				beat_Bands[i] = -beatBands[i]
				
	# Determine if any beat was detected
	beatDetected = False
	if(beat_Main >= 1):
		beatDetected = True
	else:
		for bb in beat_Bands:
			if(bb >= 1):
				beatDetected = True
	
	# Return MusicFrameData Object
	return MusicFrameData(beatDetected, beat_Main, beat_Bands)


############################################## MAIN ################################################

##### Parse Command Line Arguments #####
parser = argparse.ArgumentParser(description = "Process Command Line Arguments.")

parser.add_argument('-c', required = False, dest = "config_Loc",
					help = "Add a directory of MP3s to the Library", action = 'store')


##### Parse Config File #####

config = ConfigParser.ConfigParser()
try:
	global deviceID, sampleSize, numChannels, sampleRate, useFreqBands, numFreqBands
	global ignoreHighBand, freqRangePercentage, useDynamicTrigger, linRegConst_A, lin_RegConst_B
	global triggerConst_Main, triggerConst_Bands, useDynamicHistBuffer, histBufferSize
	
	config.read(config_loc)
	
	deviceID = config.getint(CONFIG_VARS['pyaudio'], CONFIG_VARS['deviceID'])
	sampleSize = config.getint(CONFIG_VARS['pyaudio'], CONFIG_VARS['sampleSize'])
	numChannels = config.getint(CONFIG_VARS['pyaudio'], CONFIG_VARS['numChannels'])
	sampleRate = config.getint(CONFIG_VARS['pyaudio'], CONFIG_VARS['sampleRate'])
	
	useFreqBands = config.getboolean(CONFIG_VARS['beatDetection'], CONFIG_VARS['useFreqBands'])
	numFreqBands = config.getint(CONFIG_VARS['beatDetection'], CONFIG_VARS['numFreqBands'])
	ignoreHighBand = config.getboolean(CONFIG_VARS['beatDetection'], CONFIG_VARS['ignoreHighBand'])
	freqRangePercentage_temp = config.get(CONFIG_VARS['beatDetection'], CONFIG_VARS['freqRangePercentage'])
	useDynamicTrigger = config.getboolean(CONFIG_VARS['beatDetection'], CONFIG_VARS['useDynamicTrigger'])
	linRegConst_A = config.getfloat(CONFIG_VARS['beatDetection'], CONFIG_VARS['linRegConst_A'])
	linRegConst_B = config.getfloat(CONFIG_VARS['beatDetection'], CONFIG_VARS['linRegConst_B'])
	triggerConst_Main = config.getfloat(CONFIG_VARS['beatDetection'], CONFIG_VARS['triggerConst_Main'])
	triggerConst_Bands_temp = config.get(CONFIG_VARS['beatDetection'], CONFIG_VARS['triggerConst_Bands'])
	useDynamicHistBuffer = config.getboolean(CONFIG_VARS['beatDetection'], CONFIG_VARS['useDynamicHistBuffer'])
	histBufferSize = config.getint(CONFIG_VARS['beatDetection'], CONFIG_VARS['histBufferSize'])
	
	comA = config.getint(CONFIG_VARS['lightController'], CONFIG_VARS['com_A'])
	baudA = config.getint(CONFIG_VARS['lightController'], CONFIG_VARS['baud_A'])
	comB = config.getint(CONFIG_VARS['lightController'], CONFIG_VARS['com_B'])
	baudB = config.getint(CONFIG_VARS['lightController'], CONFIG_VARS['baud_B'])
	
	triggerConst_Bands = string.split(triggerConst_Bands_temp, ',')
	for i in range(len(triggerConst_Bands)):
		triggerConst_Bands[i] = float(triggerConst_Bands[i])
		
	freqRangePercentage = string.split(freqRangePercentage_temp, ',')
	for i in range(len(freqRangePercentage)):
		freqRangePercentage[i] = float(freqRangePercentage_temp[i])
except:
	print STR_ERROR['error'] + STR_ERROR['configDNE']
	

##### Initialization #####

# Light Status/Control Objects
lights = LightStatus()
lightSelector = LightSelector(LightSelector.CONFIGS[lightConfig])
lightController = LightController(comA, baudA, comB, baudB)

# Music Analysis Objects
beatDetectors = []

if(not useFreqBands):
	numFreqBands = 0
	freqRangePercentage = [100]
	
numMade = 0
while(numMade < numFreqBands + 1):
	triggerConst = 0
	if(numMade == 0):
		triggerConst = triggerConst_Main
	else:
		triggerConst = triggerConst_Bands[numMade-1]
	beatDetectors.append(BeatDetector(	dynamicTrig = useDynamicTrigger,
										linReg_A = linRegConst_A,
										linReg_B = linRegConst_B,
										trigLevel = triggerConst,
										dynamicHist = useDynamicHistBuffer,
										histSize = histBufferSize ))

# pyAudio Object
pa = pyaudio.pyAudio()
print STR_INIT['pa_Opening']
stream = pa.open(format = PYAUDIO_FORMAT,
				 channels = numChannels,
				 input_device_index = deviceID,
				 rate = sampleRate,
				 input = True,
				 frames_per_buffer = sampleSize * numChannels)
print STR_INIT['pa_Opened']
print STR_INIT['pa_ID'] .format(deviceID)
print STR_INIT['pa_Channels'] .format(numChannels)
print STR_INIT['pa_SampRate'] .format(sampleRate)
print STR_INIT['pa_SampSize'] .format(sampleSize)
print ""


##### Main Loop #####

while(True):
	# Read Sample from Stream.
	# Data is read in the form of a string.
	# The size of each value is dependent on the format of the stream.
	# When multiple channels are streamed, the audio is interleaved.
	stream.start_stream()
	data_str = stream.read(sampleSize)
	stream.stop_stream()
	
	data_raw = fromstring(data_str, dtype=short)
	
	# De-interleave and Sum each channel to yield a mono wave
	data_Chan = zeros([sampleSize, numChannels]);
	for i in range(len(data_raw)):
		data_Chan[i/numChannels][i%numChannels] = data_raw[i];
	
	data_Summed = zeros(sampleSize);
	for i in range(sampleSize):
		data_Summed[i] = sum(data_Chan[i]);
	
	# Pass all data to first BeatDetector
	beatDetectors[0].detectBeat(data_Summed)
	
	# Take FFT and split up into frequency bands to pass to Beat Detectors
	if(numFreqBands > 0):
		data_fft = fft(data_Summed)
		
		totalPassed = 0
		for i in range(numFreqBands):
			frame = []
			for j in range(totalPassed, int(freqRangePercentage[i] * len(data_fft) + totalPassed)):
				frame.append(data_fft[j])
			
			totalPassed = int(freqRangePercentage[i] * len(data_fft) + totalPassed)
			
			beatDetectors[i+1].detectBeat(frame)
	
	# Pass to analyzeMusicFrame subroutine and Receive MusicFrameData
	musicData = analyzeMusicFrame(beatDetectors)
	
	# Pass MusicFrameData and lightStatus object to LightSelector object
	# LightSelector Object will mutate lightStatus
	lightSelector.selectLights(musicData, lights)
