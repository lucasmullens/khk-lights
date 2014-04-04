################################# BeatDetector #################################
# Author:		Dan Boehm
#
# Description:	The BeatDetector Class is responsible for storing and analyzing 
#				data necessary for beat detection.  It only detects beats for 
#				one set of data, so, for instance, if you performed an FFT on an
#				audio signal, separated the signal into several frequency bands,
#				and then wanted to perform beat detection on each band
#				simultaneously, then you would need to create a separate 
#				BeatDetector for each frequency band.
#

from scipy import *

class BeatDetector:
	##### Instance Variables #####
	#beatDetected;		# boolean: True if beat was detected
	#triggerConstant;	# float: Constant used for comparison of energyLevel to
						# 		  historyBuffer
	#triggerCalc_A		# float: Constant used for triggerConstant generation
						# 		  from equation: C = AV+B.
	#triggerCalc_B		# float: Constant used for triggerConstant generation
						#		  from equation: C = AV+B.
	#dynamicTrigger		# boolean: True if triggerConstant should be calculated
						#		   dynamically using variance and a linear
						#		   regression.
	#energyLevel;		# float: Intensity of the sample last analyzed.
	#historyBuffer;		# float[]: bufferSize past energyLevels.  Most Recent 
						#			is at pHistoryBuffer.
	#beatHistory;		# boolean[]: Past beatDetecteds aligned 
						#			 with historyBuffer
	#bufferSize;			# int: Total size of the historyBuffer.
	#pHistoryBuffer;		# int: Starting location in historyBuffer Array
	#pHistoryEnd;		# int: Last value that should be included in history 
						#	   averaging.
	#dynamicHistory;		# boolean: True if number of samples for historyBuffer
						#		   averaging should be calculated dynamically.
	
	##### Constructors #####
	
	# __init__
	#
	# Default constructor.  For parameter descriptions, see above.
	# If dynamicTrigger = False, then triggerCalc A & B must be specified.
	# Otherwise, triggerConst must be specified.
	#
	# parameters:	dynamicTrigger - boolean
	#				triggerConst - double
	#				triggerCalc_A - double
	#				triggerCalc_B - double
	#				dynamicHistory - boolean
	#				bufferSize - int
	#
	def _init_(self, dynamicTrigger, triggerConst, triggerCalc_A, triggerCalc_B,
			   dynamicHistory, bufferSize):
		self.beatDetected = False;
		self.triggerConstant = triggerConst;
		self.triggerCalc_A = triggerCalc_A;
		self.triggerCalc_B = triggerCalc_B;
		self.dynamicTrigger = dynamicTrigger;
		self.energyLevel = 0;
		self.bufferSize = bufferSize;
		self.historyBuffer = zeros(bufferSize);
		self.beatHistory = zeros(bufferSize);
		self.pHistoryBuffer = 0;
		self.pHistoryEnd = 0;
		self.dynamicHistory = dynamicHistory;
		
	##### Methods #####
	
	# getHistoryBuffer(self)
	#
	# Author:		Dan Boehm
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
		a = zeros(self.getBufferSize());
		pStart = pHistoryBuffer;
		
		for i in range(0, len(a)-1):
			a[i] = self.historyBuffer[pStart];
			p = p - 1;
			if(p < 0):
				p = bufferSize - 1;
				
		return a;
	
	# getHistoryBuffer_Full(self)
	#
	# Author:		Dan Boehm
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
		a = zeros(self.bufferSize);
		p = pHistoryBuffer;
		
		for i in range(0, bufferSize-1):
			a[i] = historyBuffer[p];
			p = p - 1;
			if(p < 0):
				p = bufferSize - 1;
				
		return a;
	
	# getBeatHistory(self)
	#
	# Author:		Dan Boehm
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
		a = zeros(self.getBufferSize());
		pStart = pHistoryBuffer;
		
		for i in range(0, len(a)-1):
			a[i] = self.beatHistory[pStart];
			p = p - 1;
			if(p < 0):
				p = bufferSize - 1;
				
		return a;
	
	# getBeatHistory_Full(self)
	#
	# Author:		Dan Boehm
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
		a = zeros(self.bufferSize);
		p = pHistoryBuffer;
		
		for i in range(0, bufferSize-1):
			a[i] = beatHistory[p];
			p = p - 1;
			if(p < 0):
				p = bufferSize - 1;
				
		return a;
	
	# gettriggerConstant(self)
	#
	# Author:		Dan Boehm
	#
	# Description:	returns the last triggerConstant used.  Be it dynamic or 
	#				static.
	#
	# Parameters: 	na
	#
	# Modifies:		none
	#
	# Returns:		A number indicating the triggerConstant last used.
	#		
	def getTriggerConstant(self):
		return self.triggerConstant;
	
	# getBufferSize(self)
	#
	# Author:		Dan Boehm
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
		return abs(self.pHistoryEnd - self.pHistoryBuffer) + 1;
	
	# getBufferCalcSize(self)
	#
	# Author:		Dan Boehm
	#
	# Description:	Returns the size of the entire historyBuffer.
	#
	# Parameters: 	na
	#
	# Modifies:		none
	#
	# Returns:		A number indicating the size of the full historyBuffer.
	#	
	def getBufferSize_Full(self):
		return self.bufferSize;

	# isDynamicTrigger(self)
	#
	# Author:		Dan Boehm
	#
	# Description:	Returns a boolean representing if the TriggerConstant is 
	#				being calculated dynamically.  This value is specified at 
	#				object construction and should not be changed.
	#
	# Parameters: 	na
	#
	# Modifies:		none
	#
	# Returns:		boolean representing if the TriggerConstant is being 
	#				calculated dynamically.
	#			
	def isDynamicTrigger(self):
		return self.dynamicTrigger;

	# isDynamicTrigger(self)
	#
	# Author:		Dan Boehm
	#
	# Description:	Returns a boolean representing if the bufferSize is 
	#				being calculated dynamically.  This value is specified at 
	#				object construction and should not be changed.
	#
	# Parameters: 	na
	#
	# Modifies:		none
	#
	# Returns:		boolean representing if the bufferSize is being 
	#				calculated dynamically.
	#					
	def isDynamicHistory(self):
		return self.dynamicHistory;

	# detectBeat(self, audioSample)
	#
	# Author:		Dan Boehm
	#
	# Description:	Returns a boolean representing if the audioSample given 
	#				represents a beat.
	#
	# Parameters: 	audioSample - Array of values representing audio intensity.
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
		energyLevel = sum(abs(audioSample));
	
		#Compute triggerLevel
		if(dynamicTrigger):
			triggerConstant = triggerCalc(self.getHistoryBuffer());
		
		# Check for beat
		if energyLevel > triggerConstant * average(self.getHistoryBuffer()):
			beatDetected = True;
		else:
			beatDetected = False;
		
		# Update History Buffer
		historyBuffer[pHistoryBuffer] = energyLevel;
		beatHistory[pHistoryBuffer] = beatDetected;
		
		pHistoryBuffer = pHistoryBuffer + 1;
		pHistoryEnd = pHistoryEnd + 1;
		if(pHistoryBuffer == bufferSize):
			pHistoryBuffer = 0;
		if(pHistoryEnd == bufferSize):
			pHistoryEnd = 0;
			
		if(dynamicHistory):
			self.historySizeCalc();
	
		# Return and Exit
		return beatDetected;
	
	# historySizeCalc(self)	#####################UNFINISHED#####################
	#
	# Author:		Dan Boehm
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
	def historySizeCalc(self):
		pass
	
	# detectBeat(history)
	#
	# Author:		Dan Boehm
	#
	# Description:	Calculates a triggerConstant from the history given. The 
	#				calculation is done based on variance.  The variance is 
	#				calculated across the history and is then entered into a 
	#				linear regression model given by the constants A & B.
	#				These values are specified during object creation and should
	#				not be modified.
	#
	# Parameters: 	history - Array of values for variance calculation
	#
	# Modifies:		none
	#
	# Returns:		Value of proper triggerConstant for the given history.
	#	
	def triggerCalc(history):
		#Compute Variance
		v = 0;
		for a in range(0, len(history)-1):
			v += history[a] - average(history);
		v = v / len(history);
	
		#Compute triggerLevel
		triggerLevel = triggerCalc_A * v + triggerCalc_B;
		
		return triggerLevel;