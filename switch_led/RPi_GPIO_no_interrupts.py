#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
import RPi.GPIO as GPIO

def main():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)  #  set pin numbering mode

    led_pin = 13
    btn_pin = 7

    GPIO.setup(led_pin, GPIO.OUT)
    GPIO.setup(btn_pin, GPIO.IN)
    
    print(GPIO.input(btn_pin))

    while(GPIO.input(btn_pin) == GPIO.LOW):
        GPIO.output(led_pin, GPIO.HIGH)
        sleep(1)
        GPIO.output(led_pin, GPIO.LOW)
        sleep(1)

    print(GPIO.input(btn_pin))

    GPIO.cleanup()

if __name__ == "__main__":
    main()