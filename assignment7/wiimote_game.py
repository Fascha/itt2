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

import time
import math

class Test(object):

    def __init__(self, wm):
        self.wm = wm


        self.have_fun()

    def set_leds_blinking(self):
        pass


    def have_fun(self):
        while True:
            patterns = [[1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0],
            [0, 1, 0, 0],
            [1, 0, 0, 0]]
            for i in range(5):
                for p in patterns:
                    self.wm.leds = p
                    # self.wm.rumble(0.1)
                    if self.wm.buttons['A']:
                        print(self.wm.accelerometer)
                        self.wm.speaker.beep()
                    time.sleep(0.05)



class Game(object):

    def __init__(self, wm):
        self.wm = wm

        # für horizontales balancieren
        self.avgx = 510
        self.avgy = 511
        self.avgz = 608

        """
        # für stehend auf ir sensor
        self.avgx = 512
        self.avgy = 612
        self.avgz = 508

        # für stehend auf unteren ende (anschluss für zusatzteile)
        self.avgx = 509
        self.avgy = 409
        self.avgz = 508

        # für auf der seite liegend (mac aufkleber oben)
        self.avgx = 613
        self.avgy = 512
        self.avgz = 510

        # für auf der seite liegend (mac aufkleber unten)
        self.avgx = 408
        self.avgy = 508
        self.avgz = 509
        """


        self.game_running = False

        self.game_loop()


    def game_loop(self):
        self.game_running = True

        # xcounter = 0
        # ycounter = 0
        # zcounter = 0
        #
        # x = []
        # y = []
        # z = []

        while self.game_running:
            ac = self.wm.accelerometer

            # counter += 1
            # if ac[0] > 0:
            #     x.append(ac[0])
            # else:
            #     xcounter += 1
            #
            # if ac[1] > 0:
            #     y.append(ac[1])
            # else:
            #     ycounter += 1
            #
            # if ac[2] > 0:
            #     z.append(ac[2])
            # else:
            #     zcounter += 1


            print(ac)

            # if ac[0] > 0 and ac[1] > 0 and ac[2] > 0:
            #     if math.fabs(ac[0] - self.avgx) > 50:
            #         self.game_over()

            if self.wm.buttons['A']:
                self.game_over()


        print("GAME OVER")
        # print("# of measures: %d" %(len(x)))
        # print("avg x: %d" % (sum(x)/len(x)))
        # print("avg y: %d" % (sum(y)/len(y)))
        # print("avg z: %d" % (sum(z)/len(z)))
        # print("x counter: %d" % (xcounter))
        # print("y counter: %d" % (ycounter))
        # print("z counter: %d" % (zcounter))
        self.wm.speaker.beep()

    def game_over(self):
        self.game_running = False

def main():

    addr_hard = 'B8:AE:6E:1B:5B:03'
    name_hard = 'Nintendo RVL-CNT-01-TR'

    input("Press the 'sync' button on the back of your Wiimote Plus " +
      "or buttons (1) and (2) on your classic Wiimote.\n" +
      "Press <return> once the Wiimote's LEDs start blinking.")

    if len(sys.argv) == 1:
        # type of both is str
        # addr, name = wiimote.find()[0]
        addr = addr_hard
        name = name_hard

    elif len(sys.argv) == 2:
        addr = sys.argv[1]
        name = None

    print(("Connecting to %s (%s)" % (name, addr)))
    wm = wiimote.connect(addr, name)
    # test = Test(wm)
    game = Game(wm)

if __name__ == '__main__':
    main()
