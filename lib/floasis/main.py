#!/usr/bin/env python

import logging
import time
import numpy as np

from lib.floasis.inputs.input_handler import InputHandler
from lib.floasis.render import renderer2d_argparser, renderer2d_from_args
from lib.floasis.animator import Animator
from lib.floasis.config import *


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

    anim = Animator(_renderer=renderer2d)
    input_handler = InputHandler(
        rotary_callback=anim.update_speed_coef,
        up_callback=anim.update_scale_0,
        left_callback=anim.update_scale_1,
        right_callback=anim.update_scale_2,
        down_callback=anim.next_anim,
    )

    while True:
        input_handler.check_input_changes()
        anim.draw()
        time.sleep(0.2)

