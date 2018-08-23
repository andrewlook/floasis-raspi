from gpiozero import Button
from time import sleep

from lib.floasis.config import *
from lib.floasis.inputs.incr_mgr import IncrementorManager


class JoystickManager(object):

    def __init__(self,
                 btn_up=None,
                 btn_down=None,
                 btn_left=None,
                 btn_right=None,
                 mgr_updown=None,
                 mgr_leftright=None):
        self.btn_up = btn_up
        self.btn_down = btn_down
        self.btn_left = btn_left
        self.btn_right = btn_right
        self.mgr_updown = mgr_updown
        self.mgr_leftright = mgr_leftright

        self.btn_up.when_pressed = self.mgr_updown.update_callback(ORDER_UP)
        self.btn_down.when_pressed = self.mgr_updown.update_callback(ORDER_DOWN)
        self.btn_left.when_pressed = self.mgr_leftright.update_callback(ORDER_DOWN) 
        self.btn_right.when_pressed = self.mgr_leftright.update_callback(ORDER_UP)


if __name__ == '__main__':

    joystick_up = Button(JOYSTICK_PINID_UP)
    joystick_down = Button(JOYSTICK_PINID_DOWN)
    joystick_left = Button(JOYSTICK_PINID_LEFT)
    joystick_right = Button(JOYSTICK_PINID_RIGHT)

    updown = IncrementorManager(name='scale_0')
    leftright = IncrementorManager(name='scale_1')

    jm = JoystickManager(btn_up=joystick_up,
                         btn_down=joystick_down,
                         btn_left=joystick_left,
                         btn_right=joystick_right,
                         mgr_updown=updown,
                         mgr_leftright=leftright)

    while True:
        sleep(0.02)
