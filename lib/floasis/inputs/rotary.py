from gpiozero import Button
from time import sleep

from lib.floasis.config import *
from lib.floasis.inputs.incr_mgr import *

class RotaryEncoder(IncrementorManager):

    def __init__(self, pin_ccw, pin_cw, **kwargs):
        super(RotaryEncoder, self).__init__(**kwargs)
        #self._ascending = True
        self.pin_ccw = pin_ccw
        self.pin_cw = pin_cw
        self.pin_ccw.when_pressed = self.update_callback(ORDER_UP)
        self.pin_cw.when_pressed = self.update_callback(ORDER_DOWN)

#     def revert_check(self):
#         if self.value > 100:
#             self._ascending = not self._ascending
#             print('REVERT {i}'.format(i=self._ascending))
#         elif self._cnt < -100:
#             self._ascending = not self._ascending
#             print('REVERT {i}'.format(i=self._ascending))
# 
#     def ccw(self):
#         if pin_cw.is_pressed:
#             self.revert_check()
#             self._cnt = self._cnt + 1 if self._ascending else self._cnt - 1
#             print('ccw {i}'.format(i=self._cnt))
# 
#     def cw(self):
#         if pin_ccw.is_pressed:
#             self.revert_check()
#             self._cnt = self._cnt - 1 if self._ascending else self._cnt + 1
#             print('cw {i}'.format(i=self._cnt))

    @property
    def value(self):
        return self.value


if __name__ == '__main__'
    pin_ccw = Button(ROTARY_PINID_COUNTERCLOCKWISE, pull_up=True)
    pin_cw = Button(ROTARY_PINID_CLOCKWISE, pull_up=True)

    rotary_encoder = RotaryEncoder(pin_ccw, pin_cw)

    while True:
        sleep(0.02)
