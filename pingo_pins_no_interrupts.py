#!/usr/bin/env python
# -*- coding: utf-8 -*-

import atexit
from time import sleep
import pingo
import RPi.GPIO as GPIO # only for warnings and cleanup

def main():
    atexit.register(GPIO.cleanup)
    GPIO.setwarnings(False)

    board = pingo.detect.get_board()
    led_pin = board.pins[13]
    led_pin.mode = pingo.OUT

    btn_pin = board.pins[7]
    btn_pin.mode = pingo.IN

    print(btn_pin.state)

    while(btn_pin.state == pingo.LOW):
        led_pin.hi()
        sleep(1)
        led_pin.lo()
        sleep(1)

    print(btn_pin.state)

    board.cleanup()

if __name__ == "__main__":
    main()