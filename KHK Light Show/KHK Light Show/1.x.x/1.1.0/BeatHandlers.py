import LightController 

################################## ChangeLights ###################################
# Author:		Dan Boehm
#
# Description:	Change the lights to a preset configuration.
#
# Parameters: 	config - Configuration to change to. Will be modded to number of
#						 configurations.
#				lightController - LightController object to use.
#
# Modifies:		none
#
# Returns:		none
#
def ChangeLights_Basic(config, lightController):
	MAX_CONFIG = 3;

	lc = lightController;

	config = config % MAX_CONFIG;

	if config == 0:
		turnOnMulti([2,9,14,16,22]);
		turnOffMulti([5,13,20,21,4,8,3,11,15,7,23]);
		lc.lightOn(19,.5);

	if config == 1:
		turnOnMulti([3,11,15,7,23]);
		turnOffMulti([2,9,14,16,22,5,13,20,21,4,8]);

	if config == 2:
		turnOnMulti([5,13,20,21,4,8]);
		turnOffMulti([2,9,14,16,22,3,11,15,7,23]);

		
		
################################### turnOnMulti ###################################
# Author:		Dan Boehm
#
# Description:	Turns on specified lights for a limited time
#
# Parameters: 	lights - Array of light IDs to turn on.
#
# Modifies:		none
#
# Returns:		none
#		
def turnOnMulti(lights):
  for i in lights:
    lc.lightOn(i, 25.5);
	
	
	
################################## turnOffMulti ###################################
# Author:		Dan Boehm
#
# Description:	Turns off specified lights.
#
# Parameters: 	lights - Array of light IDs to turn off.
#
# Modifies:		none
#
# Returns:		none
#		
def turnOffMulti(lights):
  for i in lights:
    lc.lightOn(i, 0);