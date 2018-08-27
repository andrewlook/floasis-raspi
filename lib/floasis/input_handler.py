import logging
from gpiozero import LED, Button
from time import sleep

from lib.floasis.config import *


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

MAX_VAL = 1.0
MIN_VAL = 0.0
STEP_SIZE = 0.05


class Incrementor(object):

    def __init__(self, pin_ccw, pin_cw, update_cnt):
        self._cnt = 0
        self._ascending = True
        self.pin_ccw = pin_ccw
        self.pin_cw = pin_cw
        self.update_cnt = update_cnt

        self.pin_ccw.when_pressed = self.ccw
        self.pin_cw.when_pressed = self.cw

    def revert_check(self):
        if self._cnt > MAX_VAL:
            self._ascending = not self._ascending
            logger.debug('REVERT {i}'.format(i=self._ascending))
        elif self._cnt < -MAX_VAL:
            self._ascending = not self._ascending
            logger.debug('REVERT {i}'.format(i=self._ascending))

    def ccw(self):
        if self.pin_cw.is_pressed:
            self.revert_check()
            self._update(self._cnt + 1 if self._ascending else self._cnt - 1)
            logger.debug('ccw {i}'.format(i=self._cnt))

    def cw(self):
        if self.pin_ccw.is_pressed:
            self.revert_check()
            self._update(self._cnt - 1 if self._ascending else self._cnt + 1)
            logger.debug('cw {i}'.format(i=self._cnt))

    def _update(self, newval):
        self._cnt = newval
        if self.update_cnt:
            self.update_cnt(self._cnt)


    @property
    def count(self):
        return self._cnt


class InputHandler(object):

    def __init__(self,
                 rotary_callback=None,
                 left_callback=None,
                 right_callback=None,
                 down_callback=None,
                 up_callback=None,
                 ):
        self.joystick_up = Button(JOYSTICK_PINID_UP)
        self.joystick_down = Button(JOYSTICK_PINID_DOWN)
        self.joystick_left = Button(JOYSTICK_PINID_LEFT)
        self.joystick_right = Button(JOYSTICK_PINID_RIGHT)
        self.pin_ccw = Button(ROTARY_PINID_COUNTERCLOCKWISE, pull_up=True)
        self.pin_cw = Button(ROTARY_PINID_CLOCKWISE, pull_up=True)

        self.incrementor = Incrementor(self.pin_ccw, self.pin_cw,
                                       update_cnt=rotary_callback)

        self.left_callback = left_callback
        self.right_callback = right_callback
        self.down_callback = down_callback
        self.up_callback = up_callback

    def check_input_changes(self):
        if self.joystick_up.is_pressed:
            logger.debug("up")
            if self.up_callback:
                self.up_callback()
        elif self.joystick_left.is_pressed:
            logger.debug("left")
            if self.left_callback:
                self.left_callback()
        elif self.joystick_down.is_pressed:
            logger.debug("down")
            if self.down_callback:
                self.down_callback()
        elif self.joystick_right.is_pressed:
            logger.debug("right")
            if self.right_callback:
                self.right_callback()


if __name__ == '__main__':
    input_handler = InputHandler()
    while True:
        input_handler.check_input_changes()
        sleep(0.02)
