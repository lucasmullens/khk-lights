################################### LightState ##################################
# Author:		Dan Boehm
#
# Description:	        LightState contains two classes: the LightState class and
#                       the LightStateConfigError exception.
#
#                       The LightState class keeps track of which lights are
#                       currently on.  It also decides which lights to switch on
#                       next and utilizes a LightController to actually
#                       switch them on and off.  There are several switching
#                       configurations that may be selected from upon
#                       initialization.
#
#                       The LightStateConfigError exception is thrown by the
#                       LightState class if a problem occurs during
#                       initialization.
#
# Included Modules:     LightController
#
# Copyright:            2012
#
# Developed for:        Python 2.7.1
#
# 3rd Party Modules:    na
#
#################################################################################

#################################### MODULES ####################################
import LightController



################################### CONSTANTS ###################################
STR_ERROR = {   'configError' : "The specified configuration does not exist.",
                'configDataError' : "The specified configuration parameters are \
                                     incompatible" }
CONFIG_SMART = 0
CONFIG_ROTATION = 1
CONFIG_RANDOM = 2

DEFAULT_STATE = []



##################################### CLASS #####################################
class LightState:

    ############################### STATIC METHODS ##############################



    ################################ GLOBAL VARS ################################


    
    ############################### INSTANCE VARS ###############################
    config = 0      # int - Switching configuration select
    lc = None       # LightController

    states = []     # int list - List of possible states. (not for Smart Config)
    stateID = 0     # int - index of current state in states
    
    state = []      # int list - List of lightIDs currently on.
                    #   (Smart Config only)

    
    ################################## METHODS ##################################

    ############### Constructor ###############
    #
    # Description:  Constructor Class
    #
    # Parameters:   configuration - int representing what switching method to use.
    #               configData - An object containing all info pertinant to the
    #                            selected configuration. Type varies per config.
    #               lightController - LightController used for switching.
    #
    # Returns:      na
    #
    # Throws:       LightStateConfigError - if configuration is not a valid option
    #
    def __init__(self, configuration, configData, lightController):
        self.config = configuration
        self.lc = lightController

        if self.config == CONFIG_SMART:
            self.SetupConfig_Smart(configData)
        elif self.config == CONFIG_ROTATION:
            self.SetupConfig_Rotation(configData)
        elif self.config == CONFIG_RANDOM:
            self.SetupConfig_Random(configData)
        else:
            raise LightStateConfigError(STR_ERROR['configError'])

    ############### SetupConfig_Smart ###############
    #
    # Description:  Sets up the LightState for the smart switching configuration.
    #
    # Parameters:   configData - A tuple containing the following:
    #                            (  )
    #
    # Returns:      na
    #
    # Throws:       LightStateConfigError - if configData is corrupt.
    #
    def SetupConfig_Smart(self, configData):
        pass

    ############### SetupConfig_Rotation ###############
    #
    # Description:  Sets up the LightState for the rotation switching
    #               configuration.
    #
    # Parameters:   configData - A list containing a seperate list of all
    #                            lightIDs for each state.
    #
    # Returns:      na
    #
    # Throws:       LightStateConfigError - if configData is corrupt.
    #
    def SetupConfig_Rotation(self, configData):
        if len(configData) == 0:
            raise LightStateConfigError(STR_ERROR['configDataError'])

        for s in configData:
            self.states.append(s)
        

    ############### SetupConfig_Random ###############
    #
    # Description:  Sets up the LightState for the random switching configuration.
    #
    # Parameters:   configData - A tuple containing the following:
    #                            (  )
    #
    # Returns:      na
    #
    # Throws:       LightStateConfigError - if configData is corrupt.
    #
    def SetupConfig_Random(self, configData):
        pass

    ############### SwitchState ###############
    #
    # Description:  Switches the lights to the next state based on the specified
    #               configuration.
    #
    # Parameters:   switchData - All data required to select the
    #                            next appropriate state.
    #
    # Returns:      na
    #
    # Throws:       na
    #
    def SwitchState(self, switchData):
        if self.config == CONFIG_SMART:
            self.SwitchState_Smart(switchData)
        elif self.config == CONFIG_ROTATION:
            self.SwitchState_Rotation(switchData)
        elif self.config == CONFIG_RANDOM:
            self.SwitchState_Random(switchData)


    ############### SwitchState_Smart ###############
    #
    # Description:  Switches the lights to the next state based on the smart
    #               switching algorithm.
    #
    # Parameters:   switchData - A tuple containing the following:
    #                           (  )
    #
    # Returns:      na
    #
    # Throws:       na
    #
    def SwitchState_Smart(self, switchData):
        pass


    ############### SwitchState_Rotation ###############
    #
    # Description:  Switches the lights to the next state based on the rotation
    #               switching algorithm.  If a call to SwitchState occurs when a
    #               beat was not detected, LightState reverts to the default
    #               state.
    #               
    #
    # Parameters:   beatDetected - Boolean indicating if a beat was actually
    #                              detected.
    #
    # Returns:      na
    #
    # Throws:       na
    #
    def SwitchState_Rotation(self, beatDetected):
        self.TurnOffMulti(self.states[self.stateID])

        if beatDetected:
            self.stateID = (self.stateID + 1) % len(self.states)
            self.TurnOnMulti(self.states[self.stateID])
            #print self.stateID
        

    ############### SwitchState_Random ###############
    #
    # Description:  Switches the lights to the next state based on the random
    #               switching algorithm.
    #
    # Parameters:   switchData - A tuple containing the following:
    #                           beatDetected (0) - boolean
    #                           numLights - int
    #
    # Returns:      na
    #
    # Throws:       na
    #
    def SwitchState_Random(self, switchData):
        pass

    
    ############### TurnOnMulti ###############
    #
    # Description:  Turns on all specified lights.
    #               
    #
    # Parameters:   lightIDs - A list of lightIDs to turn on.
    #
    # Returns:      na
    #
    # Throws:       na
    #
    def TurnOnMulti(self, lightIDs):
        for id in lightIDs:
            self.lc.LightOn(id)


    ############### TurnOffMulti ###############
    #
    # Description:  Turns on all specified lights.
    #               
    #
    # Parameters:   lightIDs - A list of lightIDs to turn off.
    #
    # Returns:      na
    #
    # Throws:       na
    #
    def TurnOffMulti(self, lightIDs):
        for id in lightIDs:
            self.lc.LightOff(id)
            


################################### EXCEPTION ###################################
class LightStateConfigError(Exception):
    
    ################################## METHODS ##################################

    ############### Constructor ###############
    #
    # Description:  Constructor Class
    #
    # parameters:   value - error code or cause for exception.
    #
    # returns:      na
    #
    def __init__(self, value):
        self.value = value

    ############### __str__ ###############
    #
    # Description:  Required method used to return the error value.
    #
    # parameters:   na
    #
    # returns:      string specified by value parameter during construction.
    #
    def __str__(self):
        return repr(self.value)
        
