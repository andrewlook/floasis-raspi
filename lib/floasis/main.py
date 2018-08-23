#!/usr/bin/env python

import logging
import time
import numpy as np
from gpiozero import Button

from lib.floasis.render import renderer2d_argparser, renderer2d_from_args
from lib.floasis.animator import Animator
from lib.floasis.config import *
from lib.floasis.inputs.incr_mgr import IncrementorManager
from lib.floasis.inputs.rotary import RotaryEncoder
from lib.floasis.inputs.joystick import JoystickManager


def setup_rotary():
    pin_ccw = Button(ROTARY_PINID_COUNTERCLOCKWISE, pull_up=True)
    pin_cw = Button(ROTARY_PINID_CLOCKWISE, pull_up=True)
    rotary_encoder = RotaryEncoder(pin_ccw, pin_cw,
                                   max_value=2.0,
                                   step_size=0.1)
    return rotary_encoder


def setup_joystick():
    updown = IncrementorManager(name='scale_0', min_value=1, max_value=80,
                                default_value=10, step_size=1)
    leftright = IncrementorManager(name='scale_1', min_value=1, max_value=80,
                                default_value=10, step_size=1)
    joystick_up = Button(JOYSTICK_PINID_UP)
    joystick_down = Button(JOYSTICK_PINID_DOWN)
    joystick_left = Button(JOYSTICK_PINID_LEFT)
    joystick_right = Button(JOYSTICK_PINID_RIGHT)
    joystick_mgr = JoystickManager(btn_up=joystick_up,
                                   btn_down=joystick_down,
                                   btn_left=joystick_left,
                                   btn_right=joystick_right,
                                   mgr_updown=updown,
                                   mgr_leftright=leftright)
    return updown, leftright

if __name__ == '__main__':
    parser = renderer2d_argparser()
    args = parser.parse_args()
    renderer2d = None
    while not renderer2d:
        try:
            renderer2d = renderer2d_from_args(args)
            renderer2d.load_cfg()
        except:
            print('error connecting')
            time.sleep(5)
    
    rotary_encoder = setup_rotary()
    updown, leftright = setu_joystick()

    anim = Animator(_renderer=renderer2d,
                    speed_coef_mgr=rotary_encoder,
                    scale_0_mgr=leftright,
                    scale_1_mgr=updown)

    while True:
        anim.draw()
        time.sleep(renderer2d.tick)

