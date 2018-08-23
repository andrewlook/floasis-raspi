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
    
    pin_ccw = Button(ROTARY_PINID_COUNTERCLOCKWISE, pull_up=True)
    pin_cw = Button(ROTARY_PINID_CLOCKWISE, pull_up=True)
    rotary_encoder = RotaryEncoder(pin_ccw, pin_cw,
                                   max_value=2.0,
                                   step_size=0.1)

    scale_0_mgr = IncrementorManager()
    scale_1_mgr = IncrementorManager()

    joystick_mgr = None

    anim = Animator(_renderer=renderer2d,
                    speed_coef_mgr=rotary_encoder)

#     input_handler = InputHandler(
#         rotary_callback=anim.update_speed_coef,
#         up_callback=anim.update_scale_0,
#         left_callback=anim.update_scale_1,
#         right_callback=anim.update_scale_2,
#         down_callback=anim.next_anim,
#     )

    while True:
        anim.draw()
        time.sleep(0.2)

