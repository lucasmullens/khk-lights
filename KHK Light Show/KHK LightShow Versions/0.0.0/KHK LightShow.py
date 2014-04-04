################################ KHK LightShow #################################
# Author:               Dan Boehm
#
# Version:              0.0.0
#
# Description:          KHK LightShow is a set of software and hardware designed
#                       specifically for KHK's Delta Chapter House Basement. For
#                       more info on KHK LightShow in general, please read the
#                       full documentation. The rest of this description
#                       applies specifically to the Software side of LightShow
#                       developed in Python.
#
#                       This version of KHK LightShow is a proof-of-concept more
#                       than anything. It consists of basic beat detection and
#                       light switching. Every time a beat is detected, the
#                       previous light will be turned off, and the next light
#                       will be turned on. Only one light is on at a time.
#
#                       Beat Detection is accomplished through a simple energy
#                       comparison against a localized history buffer using an
#                       arithmetic mean. All parameters involved in this
#                       algorithm are hard coded, but easily editable.
#
#                       Only one arduino may be used with this version, since it
#                       is hardcoded in. However, since LightController is
#                       scalable, the code would be easily edited to allow for
#                       multiple arduinos.
#
#                       More advanced beat detection and switching is planned
#                       for later versions. Options will also be easier to
#                       change using a config file. These changes are yet to
#                       come. 
#
# Included Modules:     LightController
#
# Copyright:            2012
#
# Developed for:        Python 2.7.1
#
# 3rd Party Modules:    PyAudio
#                       SciPy
#
################################################################################

#################################### MODULES ###################################
import pyaudio

from scipy import *
from LightController import *


################################### CONSTANTS ##################################
STR_ERROR = {	'configDNE' : "config.ini invalid or missing.  Using default \
                                values...",
                'error' : "ERROR: " }
STR_INIT = {    'pa_Opening' : "Opening Stream...",
		'pa_Opened' : "Stream opened on audio input device.",
		'pa_ID' : "\t Device ID: {}",
		'pa_Channels' : "\t Channels: {}",
		'pa_SampRate' : "\t Sample Rate: {}",
		'pa_SampSize' : "\t Sample Size: {}" }
PYAUDIO_FORMAT = pyaudio.paInt16


################################## GLOBAL VARS #################################
prevLightID = 0 #used for ChangeLight only.


################################# STATIC METHODS ###############################

############### ChangeLights ###############
#
# Description:  Filler method.  This implementation simply gives each individual
#               light its own state.
#
# parameters:   controller - The LightController object to use.
#               state - The state to set the lights to (through use of the
#                       controller.
#
# returns:      na
#
def ChangeLights(controller, state):
    global prevLightID

    # Encode lightID
    arduinoID = state / LightController.MAX_PINS
    pinID = state % LightController.MAX_PINS
    lightID = (arduinoID * 16) + pinID

    # Turn Off previous light & update
    lc.LightOff(prevLightID)
    prevLightID = lightID

    # Turn On new light
    lc.LightOn(lightID)
    


###################################### MAIN ####################################

##### Initialization #####

# Variables (To be specified in Config file)
numChannels = 1
deviceID = 0
sampleRate = 22050
sampleSize = 1024

histBuffSize = 22

arduinoPort_0 = 3

baud = 9600


# pyAudio Object
pa = pyaudio.PyAudio()
print STR_INIT['pa_Opening']
stream = pa.open(   format = PYAUDIO_FORMAT,
                    channels = numChannels,
                    input_device_index = deviceID,
                    rate = sampleRate,
                    input = True,
                    frames_per_buffer = sampleSize * numChannels )

print STR_INIT['pa_Opened']
print STR_INIT['pa_ID'] .format(deviceID)
print STR_INIT['pa_Channels'] .format(numChannels)
print STR_INIT['pa_SampRate'] .format(sampleRate)
print STR_INIT['pa_SampSize'] .format(sampleSize)
print ""

# Other
histBuff = zeros(histBuffSize)
pHistBuff = 0
beatDetected = False
sameBeat = False
triggerConst = 1.5
triggerConst_A = -0.0025714
triggerConst_B = 1.5142857

state = 0
lc = LightController([(arduinoPort_0, baud)])

##### Main Loop #####

while(True):
    # Read sample into array
    stream.start_stream()
    data = stream.read(sampleSize)  # When multiple channels are streamed, the
    stream.stop_stream()            #   audio is interleaved.

    arr_raw = zeros(len(data))
    arr_raw = fromstring(data, dtype=short)

    # De-interleave and Sum each channel to yield a mono signal
    arr_ChanData = zeros([sampleSize, numChannels])
    for i in range(len(arr_raw)):
        arr_ChanData[i/numChannels][i%numChannels] = arr_raw[i]

    arr_Summed = zeros(sampleSize)
    for i in range(sampleSize):
        arr_Summed[i] = sum(arr_ChanData[i])

    # Execute Beat Detection
    energy = sum(abs(arr_Summed))

    #varience = 0
    #for a in histBuff:
    #    varience = varience + (a - average(histBuff))
    #varience = varience / histBuffSize

    #triggerConst = triggerConst_A * varience + triggerConst_B

    if energy > (triggerConst * average(histBuff)):
        if not sameBeat:
            beatDetected = True
            sameBeat = True
        else:
            beatDetected = False
    else:
        beatDetected = False
        sameBeat = False

    # Update History Buffer
    histBuff[pHistBuff] = energy
    pHistBuff = pHistBuff + 1
    if pHistBuff == histBuffSize:
        pHistBuff = 0

    if beatDetected:
        ChangeLights(lc, state)
        state = (state + 1) % 12
        
