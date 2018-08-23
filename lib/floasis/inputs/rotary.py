from gpiozero import Button
from time import sleep

from lib.floasis.config import *
from lib.floasis.inputs.incr_mgr import *

class RotaryEncoder(IncrementorManager):

    def __init__(self, pin_ccw, pin_cw, **kwargs):
        super(RotaryEncoder, self).__init__(**kwargs)
        self._ascending = True
        self.pin_ccw = pin_ccw
        self.pin_cw = pin_cw
        self.pin_ccw.when_pressed = self.ccw
        self.pin_cw.when_pressed = self.cw

    def revert_check(self):
        if self.val + self.step_size >= self.max_value + 1e-4:
            self._ascending = not self._ascending
            print('REVERT {i}'.format(i=self._ascending))
        elif self.val - self.step_size <= self.min_value - 1e-4:
            self._ascending = not self._ascending
            print('REVERT {i}'.format(i=self._ascending))
 
    def ccw(self):
        if self.pin_cw.is_pressed:
            self.revert_check()
            direction = ORDER_UP if self._ascending else ORDER_DOWN
            self.update(direction)
            print('ccw {i}'.format(i=self.val))
 
    def cw(self):
        if self.pin_ccw.is_pressed:
            self.revert_check()
            direction = ORDER_DOWN if self._ascending else ORDER_UP
            self.update(direction)
            print('cw {i}'.format(i=self.val))


if __name__ == '__main__':
    pin_ccw = Button(ROTARY_PINID_COUNTERCLOCKWISE, pull_up=True)
    pin_cw = Button(ROTARY_PINID_CLOCKWISE, pull_up=True)

    rotary_encoder = RotaryEncoder(pin_ccw, pin_cw)

    while True:
        sleep(0.02)
