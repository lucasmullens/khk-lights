######################################### BeatDetector #############################################
# Author:		Dan Boehm
#
# Copyright: 	2011
#
# Description:	The MusicFrameData class contains all of the information necessary for the 
#				LightSelector to make its decisions.  It provides an easily accessible format for
#				aquiring all of the information it needs efficiently and in a highly organized way.
#

############################################ MODULES ###############################################



########################################### CONSTANTS ##############################################



######################################### STATIC METHODS ###########################################



############################################ CLASSES ###############################################

###################### MusicFrameData ########################
#
# Description:	MusicFrameData contains processed values from the beatDetectors' data.  It is 
#				simply a wrapper class.  It performs absolutely no data processing.
#				The MusicFrameData has a different way of representing if a beat has occured. Since 
#				All processing is done elsewhere, this standard is not actually enforced in the 
#				class and must simply just be understood.  If any beat is detected (that isn't 
#				ignored), a boolean will be set True.  This simplifies determining whether anything 
#				must be done at all.  Whether the beats actually occured is split up into two 
#				variables.  For the full waveform, the beat is represented in beat_Main.  The beat 
#				information for each frequency band is in beat_Bands.  Beat information is a float.
#				This float represents the ratio between the float and the trigger.  This allows for 
#				interpretation of how intense the beat is.  Any value less than one but greater than 
#				or equal to zero is not a beat.  A negative value means that a beat would have 
#				occured, but analyzeMusicFrame decided that the beat should be ignored.
#
# Instance Variables:	beatDetected - True if any beat was detected, False otherwise.
#						beat_Main - Float representing the overall intensity as a ratio of the
#									trigger value.
#						beat_Bands - Array of Floats for each of the frequency bands representing 
#									 the overall intensity as a ratio of the trigger value.
#
class MusicFrameData:
	##### Instance Variables #####
	beatDetected = False
	beat_Main = 0
	beat_Bands = [0]
	
	
	##### Built-in Functions #####
	def __init__(self, beatDetected, beat_Main, beat_Bands):
		self.beatDetected = beatDetected
		self.beat_Main = beat_Main
		self.beat_Bands = beat_Bands
	
	##### Functions #####