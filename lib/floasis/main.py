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
from lib.floasis.inputs.buttons import ButtonManager

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
    
    btn_args = dict(
        bounce_time=0.05,
        hold_time=0.5,
        hold_repeat=True,
    )
    red_button = Button(BUTTON_PINID_RED, **btn_args)
    blu_button = Button(BUTTON_PINID_BLU, **btn_args)
    grn_button = Button(BUTTON_PINID_GRN, **btn_args)
    whi_button = Button(BUTTON_PINID_WHI, **btn_args)
    button_mgr = ButtonManager(btn_red=red_button,
                      btn_grn=grn_button,
                      btn_blu=blu_button,
                      btn_whi=whi_button)


    updown = IncrementorManager(name='scale_0', min_value=0.0, max_value=1.0,
                                default_value=0.2, step_size=0.05)
    leftright = IncrementorManager(name='scale_1', min_value=0.0, max_value=1.0,
                                default_value=0.2, step_size=0.05)
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

    pin_ccw = Button(ROTARY_PINID_COUNTERCLOCKWISE, pull_up=True)
    pin_cw = Button(ROTARY_PINID_CLOCKWISE, pull_up=True)
    rotary_encoder = RotaryEncoder(pin_ccw, pin_cw,
                                   max_value=3.0,
                                   step_size=0.1)

    anim = Animator(_renderer=renderer2d,
                    speed_coef_mgr=rotary_encoder,
                    scale_0_mgr=leftright,
                    scale_1_mgr=updown,
                    buttons=button_mgr)

    while True:
        anim.draw()
        time.sleep(renderer2d.tick)

