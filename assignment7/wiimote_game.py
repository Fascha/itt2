#!/usr/bin/env python3
# coding: utf-8
# -*- coding: utf-8 -*-

import sys
import wiimote

import time
import random


class Game(object):

    LEDS_OFF = [0, 0, 0, 0]

    LED_PATTERNS = [[1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]]

    SEQUENCE_TO_BUTTON = {0: 'Left',
                          1: 'Up',
                          2: 'Right',
                          3: 'Down'}

    SEQUENCE_LED_DELAY = 0.5
    START_DELAY = 0.5

    def __init__(self, wm):
        self.wm = wm

        self.wm.leds = self.LEDS_OFF

        self.sequence_repeats_available = 3
        self.current_level = 0
        self.current_correct_keys = 0
        self.current_sequence = None
        self.game_running = False

        self.current_sequence_showed = False
        self.current_level_completed = False

        self.current_awaited_button = None

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

        self.display_instructions()

    def display_instructions(self):
        print("\nWelcome to WiiBop Lite!\n")
        print("Goal of WiiBop Lite is to remember a showed series of LEDs.")
        print("You will get an increasing amount of LEDs for each round.")
        print("If you get one single input wrong you will start again from scratch.")
        print("As Input you have to use the 'Arrow-Keys' which correspond to the LEDs as follows:")
        print("LED 1: Left")
        print("LED 2: Up")
        print("LED 3: Right")
        print("LED 4: Down")
        print("You have the option to show the LED sequence again by pressing the '1' Button. "
              "This feature is only available %d times so use it carefully!" % (self.sequence_repeats_available))
        print("Press the 'A' button on your WiiMote to start the Game!")

        while not self.game_running:
            if self.wm.buttons['A']:
                self.game_running = True

        self.game_loop()

    def handle_button(self, buttons):
        if len(buttons) > 0:
            if len(buttons) == 1:
                if buttons[0][0] in ['Left', 'Up', 'Right', 'Down']:
                    if buttons[0][1] is False:
                        print("awaited button", self.current_awaited_button)
                        if buttons[0][0] == self.current_awaited_button:
                            self.handle_correct_input()
                        else:
                            self.game_over()
                else:
                    # some non arrow keys pressed
                    pass
            else:
                print(buttons)

    def handle_correct_input(self):
        self.wm.rumble(0.1)
        self.current_correct_keys += 1
        if self.current_correct_keys < self.current_level:
            print("correct keys < level")
            self.current_awaited_button = self.SEQUENCE_TO_BUTTON[self.current_sequence[self.current_correct_keys]]
        elif self.current_correct_keys == self.current_level:
            print("correct keys == level => next level")
            self.next_level()
        else:
            print("SOMETHING WENT WRONG! WE SOULD NEVER GET HERE!")

    def next_level(self):
        self.current_level += 1
        self.current_correct_keys = 0
        self.current_sequence = self.generate_next_sequence(self.current_level)
        self.current_awaited_button = self.SEQUENCE_TO_BUTTON[self.current_sequence[self.current_correct_keys]]
        time.sleep(self.START_DELAY)
        self.show_current_sequence()

    def game_loop(self):
        print("GAME STARTED")
        time.sleep(1)
        self.wm.buttons.register_callback(self.handle_button)
        self.next_level()

        while self.game_running:
            if self.wm.buttons['Two']:
                self.restart()

            time.sleep(0.05)

    def show_current_sequence(self):
        print("Show current Sequence")
        print(self.current_sequence)
        for elem in self.current_sequence:
            self.wm.leds = self.LED_PATTERNS[elem]
            time.sleep(self.SEQUENCE_LED_DELAY)
            self.wm.leds = self.LEDS_OFF
            time.sleep(self.SEQUENCE_LED_DELAY)
        self.wm.leds = self.LEDS_OFF
        self.current_sequence_showed = True

    def generate_next_sequence(self, length):
        print("Generate next Sequence")
        self.current_sequence_showed = False
        seq = []
        for x in range(length):
            seq.append(random.randint(0, 3))
        return seq

    def game_over(self):
        print("GAME OVER")
        print("Your Score: %d" % self.current_level)
        self.wm.speaker.beep()
        time.sleep(1)
        self.game_running = False

    def restart(self):
        self.__init__(self.wm)


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
    game = Game(wm)


if __name__ == '__main__':
    main()
