from gpiozero import Button
from time import sleep

from lib.floasis.config import *

joystick_up = Button(JOYSTICK_PINID_UP)
joystick_down = Button(JOYSTICK_PINID_DOWN)
joystick_left = Button(JOYSTICK_PINID_LEFT)
joystick_right = Button(JOYSTICK_PINID_RIGHT)

while True:
    if joystick_up.is_pressed:
        print("up")
    elif joystick_left.is_pressed:
        print("left")
    elif joystick_down.is_pressed:
        print("down")
    elif joystick_right.is_pressed:
        print("right")
    sleep(0.02)
