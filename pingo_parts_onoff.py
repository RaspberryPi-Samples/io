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
        self.switch.set_callback_up(self.pushtype)
                
        self.recording = False
        self.GlobalState = False
        
    def loop(self):
        self.init_led_and_switch()      
        try:
            while(True):               
                time.sleep(1)

        except KeyboardInterrupt:
            print("User Cancelled (Ctrl C)")
            self.stop_at_exit()
    
    def pushtype(self):
        timer = 0
        while(self.switch.pin.state == pingo.HIGH):
            timer += 1
            time.sleep(0.1)
        if(timer <= 10):
            push_type = " short_push"
            if self.GlobalState:
                self.toggle()
        else:
            push_type = " long_push"
            self.GlobalState = not self.GlobalState
            if self.GlobalState:
                self.led.on()
                print("Power on")
            else:
                self.led.off()
                print("Power off")
        
        print(str(timer) + push_type)

    def toggle(self):
        print("press")
        self.recording = not self.recording

        if self.recording:
            self.led.blink(times=0, on_delay=0.2, off_delay=0.8) # blink forever
            self.start_recording()
        else:
            self.led.stop() # stop blinking
            self.stop_recording()
    
    def init_led_and_switch(self):
        self.led.off()
        self.switch.start()
                 
    def start_recording(self):
        print("start recording")

    def stop_recording(self):
        print("stop recording")

    def stop_at_exit(self):
        print("stopping")
        self.led.stop()
        self.led.off()
        self.switch.stop()
        self.board.cleanup()

def main():
    #atexit.register(GPIO.cleanup)
    myapp = App()
    myapp.loop()
  
if __name__ == "__main__":
    main()
