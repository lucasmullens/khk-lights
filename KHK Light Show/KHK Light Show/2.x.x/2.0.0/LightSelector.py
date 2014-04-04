######################################### LightSelector ############################################
# Author:		Dan Boehm
#
# Copyright: 	2011
#
# Description:	A Light Selector selects which lights should be on based on the past light history 
#				as well as the past/present musicFrameData.
#

############################################ MODULES ###############################################



########################################### CONSTANTS ##############################################

# Configuration Constants
GROUPS = 0


######################################### STATIC METHODS ###########################################



############################################ CLASSES ###############################################

###################### LightSelector ########################
#
# Description:	
#
# Instance Variables:	config - int
#
class BeatDetector:
	##### Instance Variables #####
	
	config = 0
	lightCtrl = None
	lights = None
	
	redID = []
	yellowID = []
	blueID = []
	greenID = []
	purpleID = []
	flash = []
	spot = []
	cyYellow = []
	cyPurple = []
	cyOrange = []
	disco = []
	
	groups = []
	nextGroup = 0
	
	
	##### Built-in Functions #####
	
	def __init__(self, lightController, config, configData, red, yellow, blue, green, purple, flash,
					spot, cyYellow, cyPurple, cyOrange, disco):
		self.config = config
		self.lightCtrl = lightController
		redID = red
		yellowID = yellow
		blueID = blue
		greenID = green
		purpleID = purple
		flashID = flash
		spotID = spot
		cyYellowID = cyYellow
		cyPurpleID = cyPurpleID
		cyOrangeID = cyOrangeID
		discoID = disco
		
		# Configuration Setup
		if(self.config == GROUPS):
			for i in range(configData[0]):	# configData[0] is numGroups
				self.groups.append([])
			
			for i in range(1, len(configData)):
				self.groups[configData[i]].append(i-1)
				
		# Setup LightStatus Object
		lights = LightStatus()
	
	##### Functions #####
	
	def selectLights(self, data):
	
		# Groups Selector
		if(self.config == GROUPS):
			if(data.beatDetected):
				prevGroup = self.nextGroup - 1
				if(prevGroup < 0):
					prevGroup = len(self.groups) - 1
				
				lightCtrl.turnOn(self.groups[self.nextGroup])
				lightCtrl.turnOff(self.groups[prevGroup])
				
				self.nextGroup = self.nextGroup + 1
				if(self.nextGroup >= len(self.groups)):
					self.nextGroup = 0