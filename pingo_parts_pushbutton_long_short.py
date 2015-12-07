#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

import atexit
from time import sleep
import RPi.GPIO as GPIO
import pingo
from pingo import LOW, HIGH
from pingo.parts.led import Led
#from pingo.parts.button import Switch

import time
import threading

class PushButton(threading.Thread):
    """Push button like component with one stable state"""

    def __init__(self, pin, time_to_sleep=0.05, 
        short_press_ticks=5, long_press_ticks=150, tick_time=0.01):
        """
        :param pin: A instance of DigitalPin
        :param time_to_sleep: time to sleep between each polling
        :param short_press_ticks: minimum number of ticks for short press (debounce switch)
        :param long_press_ticks: minimum number of ticks for a long press
        :param tick_time: duration of a tick
        """
        super(PushButton, self).__init__()
        
        self.pin = pin
        self.pin.mode = pingo.IN

        #self.lit_state = lit_state

        self.short_press_ticks = short_press_ticks
        self.long_press_ticks = long_press_ticks
        self.tick_time = tick_time

        self._press_callback = None
        self._press_long_callback = None
        self._release_callback = None

        self.active = False
        self.time_to_sleep = time_to_sleep

    def _wrap_callback(self, callback, args, kwargs):
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        def callback_wrapper():
            return callback(*args, **kwargs)
        return callback_wrapper
        
    def set_callback_pressed(self, callback, args=None, kwargs=None):
        self._press_callback = self._wrap_callback(callback, args, kwargs)

    def set_callback_pressed_long(self, callback, args=None, kwargs=None):
        self._press_long_callback = self._wrap_callback(callback, args, kwargs)

    def set_callback_released(self, callback, args=None, kwargs=None):
        self._release_callback = self._wrap_callback(callback, args, kwargs)

    def stop(self):
        self.active = False

    def run(self):
        self.active = True
        last_state = self.pin.state
        process_release = True
        while self.active:
            timer = 0
            current_state = self.pin.state
            if current_state != last_state:
                if current_state == LOW:
                    last_state = current_state
                    if process_release and self._release_callback is not None:
                        self._release_callback()
                    else:
                        process_release = True
                
                while current_state == HIGH:
                    timer += 1
                    last_state = current_state
                    current_state = self.pin.state
                    if self._press_callback is not None:
                        self._press_callback()
                    if timer >= self.long_press_ticks:
                        break
                    time.sleep(self.tick_time)
                if timer >= self.long_press_ticks and self._press_long_callback is not None:
                    self._press_long_callback()
                    process_release = False
                elif timer < self.short_press_ticks:
                    process_release = False
                else:
                    process_release = True

            time.sleep(self.time_to_sleep)

class App(object):
    def __init__(self):
        
        #GPIO.setwarnings(False)
 
        self.board = pingo.detect.get_board()

        led_pin = self.board.pins[13]
        self.led = Led(led_pin)

        self.btn_pin = self.board.pins[7]
        self.push_button = PushButton(self.btn_pin)
        self.push_button.set_callback_pressed_long(self.on_push_button_pressed_long)
        self.push_button.set_callback_released(self.on_push_button_released_short)
                
        self.recording = False
        self.global_state = True

    def loop(self):
        self.init_led_and_switch()      
        try:
            while(True):               
                time.sleep(1)

        except KeyboardInterrupt:
            logger.info("User Cancelled (Ctrl C)")
            self.stop_at_exit()

    def init_led_and_switch(self):
        self._update_led()
        self.push_button.start()

    def _update_led(self):
        if self.global_state:
            logger.info("power on")
            self.led.on()
        else:
            logger.info("power off")
            self.led.off()

    def on_push_button_pressed_long(self):
        logger.info("push button pressed long")
        self.global_state = not self.global_state
        self._update_led()

    def on_push_button_released_short(self):
        logger.info("push button released")
        self.recording = not self.recording

        if self.recording:
            self.led.blink(times=0, on_delay=0.2, off_delay=0.8) # blink forever
            self.start_recording()
        else:
            self.led.stop() # stop blinking
            self.stop_recording()
                 
    def start_recording(self):
        logger.info("start recording")

    def stop_recording(self):
        logger.info("stop recording")

    def stop_at_exit(self):
        logger.info("stopping at exit")
        self.led.stop()
        self.led.off()
        self.push_button.stop()
        self.board.cleanup()

def main():
    #logging.basicConfig(level=logging.INFO)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    #formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s")
    formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s",
                              "%Y-%m-%d %H:%M:%S")

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    atexit.register(GPIO.cleanup)
    myapp = App()
    myapp.loop()
  
if __name__ == "__main__":
    main()
