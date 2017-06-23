"""

Install the package python3-bluez_0.22-1_amd64.deb from GRIPS and follow the instructions from the slide set to get
your Wiimote working. Read the source code for wiimote.py and have a look at wiimote_demo.py to understand the API.
Write a small Python application wiimote_game.py that takes the Bluetooth MAC address of a Wiimote as its only parameter.
This application should implement a fun game that involves your WiiMote:
• The application should import wiimote similar to the wiimote_demo.py example (i.e., do not modify wiimote.py
itself).
• On launch, print instructions for the game to stdout or show them in a Qt window.
• Automatically connect to the Wiimote with the given MAC address.
• Utilize at least one input modality and one output modality of the Wiimote
• If you want, you may also implement a graphical user interface for the game - but you can also just use the Wiimote without
any display.

If you are looking for inspiration on game concepts, check out e.g., Bop It 2 or ball-in-a-maze puzzles 3 .
Hint: Activating the rumble motor will mess with the accelerometer values. You might want to wait for a short time until you read
and interpret them again.
Hand in the following file:
wiimote_game.py : a Python script that implements your game
(Please also hand in the wiimote.py version you are using)

Points
1 The python script has been submitted, is not empty, and does not print out error messages.
1 The script is well-structured and follows the Python style guide (PEP 8).
2 The game is fun to play (at least a little bit)
1 The game utilizes at least one input and one output modality of the Wiimote

"""

import sys
import wiimote



def main():
    pass

if __name__ == '__main__':
    main()
