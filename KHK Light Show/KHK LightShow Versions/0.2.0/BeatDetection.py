################################# BeatDetection #################################
# Author:		Dan Boehm
#
# Description:	        The BeatDetection module contains a number of functions
#                       that may be used to detect beats in various ways.  It
#                       also contains the MusicHistory class, which keeps track
#                       of a number of metrics required by the BeatDetection
#                       functions.  Only one BeatHistory object should be n
#
# Included Modules:     
#
# Copyright:            2012
#
# Developed for:        Python 2.7.1
#
# 3rd Party Modules:    scipy
#
#################################################################################

#################################### MODULES ####################################
from scipy import *
from math import *


################################### CONSTANTS ###################################



################################### FUNCTIONS ###################################

############### DetectBeat ###############
#
# Description:  DetectBeat is a simple beat detection function that takes in an
#               energy and compares it to the energies of localized past samples.
#
# Parameters:   energy - the energy to compare to historyBuffer
#               energyHistory - list of past energies local to the current data.
#               trigger - A constant used to compare the overall energy of data
#                         to the historyBuffer to determine beats.
#
# Returns:      boolean - True if beat was detected, else false.
#
# Throws:       none
#
def DetectBeat(energy, energyHistory, trigger):
    avgEnergy = average(energyHistory)
    
    if energy > (trigger * avgEnergy):
        return True
    
    return False    

############### CalculateEnergy ###############
#
# Description:  CalculateEnergy calculates the overall energy of a signal from a
#               set of data points.
#
# Parameters:   data - list of points on a signal. Given as floats.
#
# Returns:      float - calculated energy
#
# Throws:       none
#
def CalculateEnergy(data):
    energy = 0
    for i in range(len(data)):
        energy = energy + pow(data[i], 2)
    #print energy
    return energy

############### calculateEnergies_FFT ###############
#
# Description:  
#
# Parameters:   
#
# Returns:      
#
# Throws:       
#
def calculateEnergies_FFT(signal, numBands):
    freqSignal = fft(signal)
    
    avgEnergy = freqSignal[0]
    
    numPoints = len(freqSignal) / 2
    pointsPerBand = numPoints/numBands

    energies = []

    for i in range(len(freqSignal)):
        thisBand = []
        for j in range(pointsPerBand):
            thisBand.append(freqSignal[j+i])
            
        energies.append(CalculateEnergy(thisBand))
        
        if len(energies) == numBands:
            return energies

    return energies
    
        
    

#################################### CLASSES ####################################
class MusicHistory:
    ############################### INSTANCE VARS ###############################
    histEnergy = []   # float list - list of past energies.
    p = 0           # int - index of oldest value in history.
    histBeat = []   # boolean list - list of past beat history.

    
    ################################## METHODS ##################################

    ############### Constructor ###############
    #
    # Description:  Constructor Class
    #
    # Parameters:   historySize - number of points of history to keep.
    #
    # Returns:      na
    #
    # Throws:       na
    #
    def __init__(self, historySize):
        for i in range(historySize):
            self.histBeat.append(False)
            self.histEnergy.append(0)
    
    ############### addToEnergyHistory ###############
    #
    # Description:  Adds an data to the history Buffer. 
    #
    # Parameters:   energy - energy value to add.
    #
    # Returns:      na
    #
    # Throws:       na
    #
    def addToHistory(self, energy, beatDetected):
        self.histEnergy[self.p] = energy
        self.histBeat[self.p] = beatDetected
        self.p = (self.p + 1) % len(self.histEnergy)
