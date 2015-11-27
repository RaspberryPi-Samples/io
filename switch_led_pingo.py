#!/usr/bin/env python
# -*- coding: utf-8 -*-

import atexit
from time import sleep
#import RPi.GPIO as GPIO
import pingo
from pingo.parts.led import Led
from pingo.parts.button import Switch

import time

class App(object):
    def __init__(self):
        
        #GPIO.setwarnings(False)

        self.board = pingo.detect.get_board()

        led_pin = self.board.pins[13]
        self.led = Led(led_pin)

        self.btn_pin = self.board.pins[7]
        self.switch = Switch(self.btn_pin)
        self.switch.set_callback_up(self.press)
        self.switch.set_callback_down(self.release)
        
    def loop(self):
        self.led.off()
        self.switch.start()
        #self.led.blink(times=0) # blink foreever

        try:
            while(True):               
                time.sleep(1)

        except KeyboardInterrupt:
            print("User Cancelled (Ctrl C)")
            self.stop_at_exit()

    def press(self):
        print("press")
        self.toggle()
  
    def release(self):
        print("release")
        
    def toggle(self):
        self.led.toggle()

    def stop_at_exit(self):
        self.led.off()
        self.switch.stop()
        self.led.stop()
        self.board.cleanup()


def main():
    #atexit.register(GPIO.cleanup)
    myapp = App()
    myapp.loop()
  
if __name__ == "__main__":
    main()
