############################## CollectAudioStats ###############################
# Author:               Dan Boehm
#
# Version:              1.0.0
#
# Description:          CollectAudioStats is a simple script designed to take
#                       several sound energy data points using PyAudio, and then
#                       analyze them and display statistics on that data.
#
#                       The results of this data was originally intended to be
#                       used for determining the min energy that should be
#                       considered audio by KHK LightShow's Beat Detection
#                       algorithm.
#
#                       This software displays only statistics collected from
#                       the time domain of the wave.  In future versions,
#                       data collection accross the fequency domain may be
#                       added.
#
#                       CollectAudioStats requires a config file.  It is
#                       suggested that the config file from the LightShow
#                       version to be used is copied into the CollectAudioStats
#                       directory for use.
#
# Included Modules:     na
#
# Copyright:            2012
#
# Developed for:        Python 2.7.1
#
# 3rd Party Modules:    PyAudio
#                       ConfigParser*
#
#                       * Module included with Python 2.7.1
#
################################################################################

#################################### MODULES ###################################
import pyaudio
import ConfigParser

from scipy import *


################################### CONSTANTS ##################################
STR_CNFG = {    'pa' : "PyAudio",
                'pa_chans' : "Channels",
                'pa_devID' : "AudioIn_DeviceID",
                'pa_sampRate' : "SampleRate",
                'pa_sampSize' : "SampleSize" }
STR_MAIN = {    'data' : "Collecting Data...\n",
                'welcome' : "Initializing...\n",
                'results' : "Results:\n",
                'ready' : "Ready to collect data.\n\n\tHow many data points? \
                            \n\n>>> " }
STR_INIT = {    'pa_Opening' : "Opening Stream...",
		'pa_Opened' : "Stream opened on audio input device.",
		'pa_ID' : "\t Device ID: {}",
		'pa_Channels' : "\t Channels: {}",
		'pa_SampRate' : "\t Sample Rate: {}",
		'pa_SampSize' : "\t Sample Size: {}" }
STR_RESULTS = { 'num' : "  Data Points Collected: {}",
                'max' : "Maximum Energy Recorded: {}",
                'min' : "Minimum Energy Recorded: {}",
                'avg' : "        Arithmetic Mean: {}",
                'var' : "               Varience: {}" }
PYAUDIO_FORMAT = pyaudio.paInt16

##################################### MAIN #####################################

print STR_MAIN['welcome']

##### Read Config #####
config = ConfigParser.ConfigParser()

config.read("config.ini")

numChannels = config.getint(STR_CNFG['pa'], STR_CNFG['pa_chans'])
deviceID = config.getint(STR_CNFG['pa'], STR_CNFG['pa_devID'])
sampleRate = config.getint(STR_CNFG['pa'], STR_CNFG['pa_sampRate'])
sampleSize = config.getint(STR_CNFG['pa'], STR_CNFG['pa_sampSize'])

##### Initialization #####
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

maxPoints = int(raw_input(STR_MAIN['ready']))

numPoints = 0
points = []
maxEnergy = 0
minEnergy = int(0x7FFFFFF)  # max positive int value
avgEnergy = 0
varience = 0

while numPoints < maxPoints:
    print numPoints
    
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

    # Calculate Energy
    energy = 0
    for i in range(len(arr_Summed)):
        energy = energy + pow(arr_Summed[i], 2)

    # Add to statistics
    points.append(energy)
    numPoints = numPoints + 1

    if energy > maxEnergy:
        maxEnergy = energy

    if energy < minEnergy:
        minEnergy = energy

# Finalize Statistics
avgEnergy = average(points)

for x in points:
    varience = varience + pow((x - average(points)), 2)
varience = varience / numPoints

# Print Statistics
print STR_MAIN['results']
print STR_RESULTS['num'] .format(numPoints)
print STR_RESULTS['max'] .format(maxEnergy)
print STR_RESULTS['min'] .format(minEnergy)
print STR_RESULTS['avg'] .format(avgEnergy)
print STR_RESULTS['var'] .format(varience)
