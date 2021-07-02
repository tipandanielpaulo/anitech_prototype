# !/bin/python

import RPi.GPIO as GPIO
import time

import os
import I2C_LCD_driver

GPIO.setmode(GPIO.BCM)
GPIO.setup(27,GPIO.IN, pull_up_down=GPIO.PUD_UP)

def Shutdown(channel):
	mylcd = I2C_LCD_driver.lcd()
	print("Shutting Down")
	time.sleep(5)

	mylcd.lcd_display_string("Shutting down....")
	os.system("sudo shutdown -h now")

GPIO.add_event_detect(27, GPIO.FALLING, callback=Shutdown, bouncetime=2000)

while 1:
	time.sleep(1)
