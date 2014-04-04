################################ KHK LightShow #################################
# Author:               Dan Boehm
#
# Version:              0.2.0
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
#                       arithmetic mean. All parameters involved are specified
#                       in config.ini.
#
#                       More advanced beat detection and switching is planned
#                       for later versions.
#
# Included Modules:     LightController
#                       LightState
#                       BeatDetection
#
# Copyright:            2012
#
# Developed for:        Python 2.7.1
#
# 3rd Party Modules:    PyAudio
#                       SciPy
#                       ConfigParser*
#                       string*
#
#                       * module included with Python 2.7.1
#
################################################################################

#################################### MODULES ###################################
import pyaudio
import ConfigParser
import string
import LightController
import LightState

from scipy import *
from BeatDetection import *


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
STR_CNFG = {    'pa' : "PyAudio",
                'pa_chans' : "Channels",
                'pa_devID' : "AudioIn_DeviceID",
                'pa_sampRate' : "SampleRate",
                'pa_sampSize' : "SampleSize",
                'lc' : "Light Controller",
                'lc_ports' : "ArduinoPorts",
                'lc_baud' : "BaudRate",
                'bd' : "Beat Detection",
                'bd_histBuffSize' : "HistoryBufferSize",
                'bd_dynamicTrig' : "UseDynamicTrigger",
                'bd_trig' : "TriggerConstant",
                'bd_m' : "TriggerLinReg_m",
                'bd_b' : "TriggerLinReg_b",
                'sw' : "Switching",
                'sw_smart' : "Smart",
                'sw_rot' : "Rotation",
                'sw_rand' : "Random",
                'smartSw' : "Smart Switching",
                'rotSw' : "Rotation Switching",
                'rotSw_num' : "NumStates",
                'rotSw_stateX' : "state{}",
                'randSw' : "Random Switching" }
PYAUDIO_FORMAT = pyaudio.paInt16


################################## GLOBAL VARS #################################



################################# STATIC METHODS ###############################
    


###################################### MAIN ####################################

##### Read Config File #####
config = ConfigParser.ConfigParser()

config.read("config.ini")

# PyAudio Config
numChannels = config.getint(STR_CNFG['pa'], STR_CNFG['pa_chans'])
deviceID = config.getint(STR_CNFG['pa'], STR_CNFG['pa_devID'])
sampleRate = config.getint(STR_CNFG['pa'], STR_CNFG['pa_sampRate'])
sampleSize = config.getint(STR_CNFG['pa'], STR_CNFG['pa_sampSize'])

# LightController Config & initialization
baud = config.getint(STR_CNFG['lc'], STR_CNFG['lc_baud'])
arduinos = string.split(config.get(STR_CNFG['lc'], STR_CNFG['lc_ports']), ', ')

serials = []
for a in arduinos:
   serials.append((int(a), baud))
   
lc = LightController.LightController(serials)

# Beat Detection Config
histBuffSize = config.getint(STR_CNFG['bd'], STR_CNFG['bd_histBuffSize'])
triggerConst = config.getfloat(STR_CNFG['bd'], STR_CNFG['bd_trig'])

# LightState Config & Initialization
lights = None

switchConfig = -1
if config.getboolean(STR_CNFG['sw'], STR_CNFG['sw_smart']):
    switchConfig = LightState.CONFIG_SMART
    
elif config.getboolean(STR_CNFG['sw'], STR_CNFG['sw_rot']):
    switchConfig = LightState.CONFIG_ROTATION
    numStates = config.getint(STR_CNFG['rotSw'], STR_CNFG['rotSw_num'])
    
    states = []
    for i in range(numStates):
        thisState = config.get(STR_CNFG['rotSw'],
                               STR_CNFG['rotSw_stateX'] .format(i))
        states.append(string.split(thisState, ', '))
    for i in range(len(states)):
        for j in range(len(states[i])):
            states[i][j] = int(states[i][j], 16)
    print states

    lights = LightState.LightState(switchConfig, states, lc)
        
elif config.getboolean(STR_CNFG['sw'], STR_CNFG['sw_rand']):
    switchConfig = LightState.CONFIG_RANDOM


##### Initialization #####

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
history = MusicHistory(histBuffSize)
beatDetected = False


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
    energy = CalculateEnergy(arr_Summed)
    
    beatDetected = DetectBeat(energy, history.histEnergy, triggerConst)

    # Update History Buffer
    history.addToHistory(energy, beatDetected)

    if beatDetected:
        lights.SwitchState(beatDetected)
        
