######################################### BeatDetector #############################################
# Author:		Dan Boehm
#
# Copyright: 	2011
#
# Description:	The BeatDetector Class is responsible for storing and analyzing 
#				data necessary for beat detection.  It only detects beats for 
#				one set of data, so, for instance, if you performed an FFT on an
#				audio signal, separated the signal into several frequency bands,
#				and then wanted to perform beat detection on each band
#				simultaneously, then you would need to create a separate 
#				BeatDetector for each frequency band.
#

############################################ MODULES ###############################################

from scipy import zeros
from numpy import average


########################################### CONSTANTS ##############################################



######################################### STATIC METHODS ###########################################

###################### calcTriggerLevel ########################
#
# Description:	Calculates a triggerConstant from the history given. The 
#				calculation is done based on variance.  The variance is 
#				calculated across the history and is then entered into a 
#				linear regression model given by the specified values.
#
# Parameters: 	history - Array of values for variance calculation
#				slope - Slope value of the linear regression model
#				intercept - Y-Intercept value of the linear regression model
#
# Modifies:		none
#
# Returns:		Value of proper triggerConstant for the given history and regression.
#	
def calcTriggerLevel(history, slope, intercept):
	#Compute Variance
	v = 0
	for a in range(0, len(history)-1):
		v += history[a] - average(history)
	v = v / len(history)

	#Compute triggerLevel
	triggerLevel = slope * v + intercept
	
	return triggerLevel
	


############################################ CLASSES ###############################################

###################### BeatDetector ########################
#
# Description:	
#
# Instance Variables:	beatDetected - boolean
#						beatHistory - boolean[]
#						bufferSize - int
#						dynamicHistory - boolean
#						dynamicTrigger - boolean
#						energyLevel - float
#						historyBuffer - float[]
#						pHistoryBuffer - int
#						pHistoryEnd - int
#						triggerConst_A - float
#						triggerConst_B - float
#						triggerConst - float
#
class BeatDetector:
	##### Instance Variables #####
	beatDetected = False
	beatHistory = []
	bufferSize = 0
	dynamicHistory = False
	dynamicTrigger = False
	energyLevel = 0
	historyBuffer = []
	pHistoryBuffer = 0
	pHistoryEnd = 0
	triggerConst_A = 0
	triggerConst_B = 0
	triggerConst = 0
	
	
	##### Built-in Functions #####
	
	def __init__(self, bufferSize, dynamicHistory, dynamicTrigger, triggerConst):
		self.bufferSize = bufferSize
		self.dynamicHistory = dynamicHistory
		self.dynamicTrigger = dynamicTrigger
		self.triggerConst = triggerConst
		
		self.beatHistory = zeros(bufferSize)
		self.historyBuffer = zeros(bufferSize)
		self.pHistoryEnd = bufferSize-1
		
	
	##### Functions #####
	
	###################### getHistoryBuffer ########################
	#
	# Description:	returns the historyBuffer used to calculate last beatDetect.
	#
	# Parameters: 	na
	#
	# Modifies:		none
	#
	# Returns:		An array representing the History Buffer used for
	#				calculations.  The most recent value is stored at location 
	#				0.
	#
	def getHistoryBuffer(self):
		a = zeros(self.getBufferSize())
		pStart = pHistoryBuffer
		
		for i in range(len(a)):
			a[i] = self.historyBuffer[pStart]
			p = p - 1
			if(p < 0):
				p = bufferSize - 1
				
		return a	
	
	################### getHistoryBuffer_Full ######################
	#
	# Description:	returns the entire historyBuffer
	#
	# Parameters: 	na
	#
	# Modifies:		none
	#
	# Returns:		An array containing every stored sample in History.  The
	#				most recent value is stored at location 0.
	#	
	def getHistoryBuffer_Full(self):
		a = zeros(self.bufferSize)
		p = pHistoryBuffer
		
		for i in range(bufferSize):
			a[i] = historyBuffer[p]
			p = p - 1
			if(p < 0):
				p = bufferSize - 1
				
		return a
		
	##################### getBeatHistory #########################
	#
	# Description:	returns the beatHistory corresponding to the array returned 
	#				by getHistoryBuffer(self).
	#
	# Parameters: 	na
	#
	# Modifies:		none
	#
	# Returns:		An array containing booleans representing beats.  One-to-one
	#				correspondance to the array returned by 
	#				getHistoryBuffer(self).
	#		
	def getBeatHistory(self):
		a = zeros(self.getBufferSize())
		pStart = pHistoryBuffer
		
		for i in range(len(a)):
			a[i] = self.beatHistory[pStart]
			p = p - 1
			if(p < 0):
				p = bufferSize - 1
				
		return a
	
	################### getBeatHistory_Full ######################
	#
	# Description:	returns the beatHistory corresponding to the array returned 
	#				by getHistoryBuffer_Full(self).
	#
	# Parameters: 	na
	#
	# Modifies:		none
	#
	# Returns:		An array containing booleans representing beats.  One-to-one
	#				correspondance to the array returned by 
	#				getHistoryBuffer_Full(self).
	#		
	def getBeatHistory_Full(self):
		a = zeros(self.bufferSize)
		p = pHistoryBuffer
		
		for i in range(bufferSize):
			a[i] = beatHistory[p]
			p = p - 1
			if(p < 0):
				p = bufferSize - 1
				
		return a

	################### getBufferSize ######################
	#
	# Description:	Returns the size of the part of the historyBuffer last used
	#				for calculations.
	#
	# Parameters: 	na
	#
	# Modifies:		none
	#
	# Returns:		A number indicating the size of the historyBuffer last used.
	#	
	def getBufferSize(self):
		return abs(self.pHistoryEnd - self.pHistoryBuffer) + 1
		
	################### detectBeat ######################
	#
	# Description:	Returns a boolean representing if the audioSample given 
	#				represents a beat.
	#
	# Parameters: 	audioSample - Array of values representing audio intensity over time.
	#
	# Modifies:		energyLevel
	#				beatDetected
	#				historyBuffer
	#				beatHistory
	#				triggerConstant (if dynamicTrigger = True)
	#				pHistoryBuffer
	#
	# Returns:		boolean representing if a beat was detected.
	#			
	def detectBeat(self, audioSample):
		# Calculate instant sound energy
		energyLevel = sum(abs(audioSample))
	
		#Compute triggerLevel
		if(dynamicTrigger):
			triggerConstant = calcTriggerLevel(self.getHistoryBuffer(), self.triggerConst_A, 
											self.triggerConst_B)
		
		# Check for beat
		if energyLevel > triggerConstant * average(self.getHistoryBuffer()):
			beatDetected = True
		else:
			beatDetected = False
		
		# Update History Buffer
		historyBuffer[pHistoryBuffer] = energyLevel
		beatHistory[pHistoryBuffer] = beatDetected
		
		pHistoryBuffer = pHistoryBuffer + 1
		pHistoryEnd = pHistoryEnd + 1
		if(pHistoryBuffer == bufferSize):
			pHistoryBuffer = 0
		if(pHistoryEnd == bufferSize):
			pHistoryEnd = 0
			
		if(dynamicHistory):
			self.calcHistBuffSize()
	
		# Return and Exit
		return beatDetected
	
	################### calcHistBuffSize ######################
	#
	# Description:	Analyzes the Beat History, and lengthens or shortens the 
	#				historyBuffer accordingly.
	#
	# Parameters: 	none
	#
	# Modifies:		pHistoryEnd
	#
	# Returns:		none
	#	
	def calcHistBuffSize(self):
		pass
		################ UNFINISHED ##################