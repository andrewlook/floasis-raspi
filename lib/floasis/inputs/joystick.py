from gpiozero import Button
from time import sleep

from lib.floasis.config import *

joystick_up = Button(JOYSTICK_PINID_UP)
joystick_down = Button(JOYSTICK_PINID_DOWN)
joystick_left = Button(JOYSTICK_PINID_LEFT)
joystick_right = Button(JOYSTICK_PINID_RIGHT)

pin_ccw = Button(ROTARY_PINID_COUNTERCLOCKWISE, pull_up=True)
pin_cw = Button(ROTARY_PINID_CLOCKWISE, pull_up=True)

class Incrementor(object):

    def __init__(self, pin_ccw, pin_cw):
        self._cnt = 0
        self._ascending = True
        self.pin_ccw = pin_ccw
        self.pin_cw = pin_cw

        self.pin_ccw.when_pressed = self.ccw
        self.pin_cw.when_pressed = self.cw

    def revert_check(self):
        if self._cnt > 100:
            self._ascending = not self._ascending
            print('REVERT {i}'.format(i=self._ascending))
        elif self._cnt < -100:
            self._ascending = not self._ascending
            print('REVERT {i}'.format(i=self._ascending))

    def ccw(self):
        if pin_cw.is_pressed:
            self.revert_check()
            self._cnt = self._cnt + 1 if self._ascending else self._cnt - 1
            print('ccw {i}'.format(i=self._cnt))

    def cw(self):
        if pin_ccw.is_pressed:
            self.revert_check()
            self._cnt = self._cnt - 1 if self._ascending else self._cnt + 1
            print('cw {i}'.format(i=self._cnt))

    @property
    def count(self):
        return self._cnt

incrementor = Incrementor(pin_ccw, pin_cw)

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
