--- System Requirements ---

- Windows OS (tested with XP and 7x64)
- Some type of Audio-Input (ie: microphone, line in, etc)
- Python 2.7.1 and required modules.
- USB ports for communication with Arduinos


--- Installation ---

KHK LightShow requires several pieces of software in order to work.

First, the KHK LightShow software requires the following software to be installed:
	- Python 2.7.1
	- PyAudio
	- SciPy

Setup files for the above can be found in the "Installation" directory.

KHK LightShow relies on Arduinos to provide power to the digital inputs on the switching relays.  These arduinos communicate with the PC and are powered over USB.  Occasionally drivers need to be installed for a PC to recognise the Arduinos.  The driver needed may vary, but the only known incidence of this, so far, is the driver for the UART communications chipset on the Arduino Board.  The working driver as of 1/14/2012 may be found in the "Drivers" directory.  Other necessary drivers for the arduino exist, but vary from board to board.  All of these drivers are included along with the Arduino IDE, which may be downloaded at the arduino homepage.

The arduinos themselves also must be uploaded with the proper software.  The raw code may be found in the "Installation\Arduino Software" directory.  This software must be uploaded via the Arduino IDE.

This covers all software related installation.  Hardware documentation is covered in a seperate document.


--- Using KHK Light Show ---

Assuming proper hardware installation, using KHK Lightshow is very simple.

To Run:
	1) run "KHK LightShow.bat".
	2) Observe that the window that appears does not display errors.

To Exit:
	1) Close the window that appeared on startup.


--- Editing Config.ini ---

Many program parameters can be changed through editing the Config.ini file.  It is recommended that Config.ini is backed up before making any changes.  It is important that item names and section names are not edited.  Only values should be changed.

Every item can have a different type of value.  It is important that values types are not changed.  For a full list of items and their corresponding type, see the full documentation.

Boolean values should be represented with a 1 (true) or a 0 (false).

Arrays should be represented in one line with each item seperated by a comma followed by a single space (", ").

KHK LightShow will not work without Config.ini.  It is important that this file is not deleted or renamed.


--- Troubleshooting ---

Problem: KHK LightShow does not indicate an error, but lights are switching sporadically or not switching at all.

Probable Cause: The audio setup is incorrect.

Solution: LightShow requires the audio-out signal to be fed into an audio-in device on the PC in some manner.  The intended method for this is to split the audio-out signal as it leaves the PC's sound card, and have one side of the split connect to the microphone port on the soundcard, while the other end goes to the audio system.  The Config file tells Lightshow which audio-in device to use.  Window's default audio device is always '0' (zero).


Problem: KHK LightShow displays an error on startup that says it can't connect to COM #.

Probable Cause: LightShow thinks the arduino is connected to a different COM port than it actually is.

Solution: Change the COM Ports in the config file.  The correct port numbers can be found in Windows' Device Manager (Control Panel -> System -> Device Manager).


Problem: KHK LightShow appears to startup correctly but no lights will turn on.

Probable Cause: Incorrect Hardware Setup

Solution: Consult other documentation and check that all hardware is connected properly.  If there is a hardware problem is is most likely due to something being unplugged.  Check that all arduino pins are plugged in.  Check that the CAT-V cables are connected at both ends.  Check that the Switching Modules are pluged into a AC Source.  Check that that AC source has power.  If none of these are the problem, it is likely that some part of the hardware system has broken, and more in-depth troubleshooting will be required.