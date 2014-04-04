################################ LightController ################################
# Author:		Dan Boehm
#
# Description:	        The LightController class facilitates serial
#                       communication between the KHK LightShow software and the
#                       arduinos.
#
#                       Information is passed to the LightController via a
#                       lightID.  A lightID consists of an int that, when
#                       represented by a hex string, easily describes
#                       both the arduino ID and the local pinID corresponding to
#                       that particular light.  For example '0x00' represents the
#                       0th light controlled by arduino 0 (or rather pin 0 on
#                       arduino 0), while '0x1B' represents the 11th light
#                       controlled by arduino 1 (pin 13 on arduino 1).
#
#                       Because of the implementation of lightID and
#                       initialization of the class, a LightController is
#                       completely scalable.  The only limitation on the number
#                       of arduinos that may be controlled is the number of
#                       available serial ports.
#
#                       This module is heavily based on Samuel Hurley's work.
#
# Included Modules:     na
#
# Copyright:            2012
#
# Developed for:        Python 2.7.1
#
# 3rd Party Modules:    pySerial
#
#################################################################################

#################################### MODULES ####################################
import serial


##################################### CLASS #####################################
class LightController:

    ################################# CONSTANTS #################################
    START_BYTE = 255
    ON = 1
    OFF = 0
    MAX_PINS = 12

    ############################### STATIC METHODS ##############################



    ################################ GLOBAL VARS ################################


    
    ############################### INSTANCE VARS ###############################
    arduinos = [] # A list of arduino serial communication ports.

    
    ################################## METHODS ##################################

    ############### Constructor ###############
    #
    # Description:  Constructor Class
    #
    # parameters:   arduinoPorts - An array of tuples in the form of
    #                               (COM Port, Baud Rate)
    #
    # returns:      na
    #
    def __init__(self, arduinoPorts):
        # Open a serial connection to each Arduino
        for a in arduinoPorts:
            self.arduinos.append(serial.Serial(a[0], a[1]))
            

    ############### lightOn ###############
    #
    # Description:  Turns the specified light on. If lightID is invalid, this
    #               method will do nothing.
    #
    # parameters:   lightID - An integer specifying the light ID.
    #                           (see lightID note in class description).
    #
    # returns:      na
    #
    def LightOn(self, lightID):
        # Decode the lightID.
        hexID = hex(lightID)
        #print hexID
        
        arduinoID = 0 # case for '0x' + pinID (accounts for aID = 0 case)
        if len(hexID) < 3: # not valid lightID
            return
        elif len(hexID) > 3:
            arduinoID = int(hexID[len(hexID) - 1 - 1]) # last index minus pinID
        #print arduinoID
        
        pinID = int(hexID[len(hexID) - 1], 16) # last index
        #print pinID

        # Check for valid lightID
        if arduinoID >= len(self.arduinos) or pinID >= self.MAX_PINS:
            return

        # Write data to serial port
        self.arduinos[arduinoID].write(chr(self.START_BYTE))
        self.arduinos[arduinoID].write(chr(pinID))
        self.arduinos[arduinoID].write(chr(self.ON))

    ############### lightOff ###############
    #
    # Description:  Turns the specified light off. If lightID is invalid, this
    #               method will do nothing.
    #
    # parameters:   lightID - An integer specifying the light.
    #                           (see lightID note in class description).
    #
    # returns:      na
    #   
    def LightOff(self, lightID):
        # Decode the lightID.
        hexID = hex(lightID)
        #print hexID
        
        arduinoID = 0 # case for '0x' + pinID (accounts for aID = 0 case)
        if len(hexID) < 3: # not valid lightID
            return
        elif len(hexID) > 3:
            arduinoID = int(hexID[len(hexID) - 1 - 1]) # last index minus pinID
        #print arduinoID
        
        pinID = int(hexID[len(hexID) - 1], 16) # last index
        #print pinID
        
        # Check for valid lightID
        if arduinoID >= len(self.arduinos) or pinID >= self.MAX_PINS:
            return
        
        # Write data to serial port
        self.arduinos[arduinoID].write(chr(self.START_BYTE))
        self.arduinos[arduinoID].write(chr(pinID))
        self.arduinos[arduinoID].write(chr(self.OFF))
