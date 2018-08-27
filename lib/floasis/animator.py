#!/usr/bin/env python

import logging
import time
import numpy as np

from lib.floasis.animations import ANIMATIONS, ALL_ANIMS
from lib.floasis.input_handler import InputHandler
from lib.floasis.render import renderer2d_argparser, renderer2d_from_args
from lib.floasis.config import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Animator(object):

    def __init__(self,
                 _renderer,
                 scale_0_mgr,
                 scale_1_mgr,
                 speed_coef_mgr):
        self.renderer = _renderer

        self.scale_0_mgr = scale_0_mgr
        self.scale_1_mgr = scale_1_mgr
        self.speed_coef_mgr = speed_coef_mgr

        # time step - makes the animation move
        self.counter = 0

        # variables controlled by inputs, shared across animations
        #self.scale_0 = DEFAULT_SCALE_0
        #self.scale_0_order = 'UP'
        #self.scale_1 = DEFAULT_SCALE_1
        #self.scale_1_order = 'UP'
        #self.scale_2 = DEFAULT_SCALE_2
        #self.scale_2_order = 'UP'
        
        #self.speed_coef = DEFAULT_SPEED_COEF

        # which animation to do
        self.anim_num = 0

    

    # TODO(look) replace this with the button handler
    def anim_func(self):
        """ get the current animation function safely - if anything is
        misconfigured, use a default animation function. """
        return ANIMATIONS.get(self.anim_name, DEFAULT_ANIMATION_FUNC)

    # TODO(look) replace this with the button handler
    @property
    def anim_name(self):
        return ALL_ANIMS[self.anim_num]

    # TODO(look) replace this with the button handler
    def next_anim(self):
        old_anim = self.anim_num
        self.anim_num = (self.anim_num + 1) % NUM_ANIMS
        new_anim = self.anim_name
        print('{o} -> {n}'.format(o=old_anim, n=new_anim))

    def update_speed_coef(self, newval):
        sigmoided = 1 / (1 + np.exp(-newval))
        self.speed_coef = MIN_SPEED_COEF + (sigmoided * MAX_SPEED_COEF)
        print('speed_coef = {c} (newval = {n}, sigmoided = {s})'
                    .format(c=self.speed_coef, n=newval, s=sigmoided))

    def draw(self):
        # get the current animation function
        xy_func = self.anim_func()

        pixels = [(0, 0, 0)] * renderer2d.led_num
        # TODO(look): i vs. ordinal position for missing pixels?
        for i, coord in enumerate(renderer2d.ord_to_xy):
            x, y = coord
            # if the x/y values in the map were -1, (meaning the config
            # file says to ignore this pixel), render black for this pixel
            if x < 0 or y < 0:
                continue

            color = xy_func(x, y,
                            cnt=self.counter,
                            scale_0=self.scale_0,
                            scale_1=self.scale_1,
                            speed_coef=self.speed_coef)
            pixels[i] = color

            # print('i = {i}   ( x = {x}, y = {y} )  {c}'.format(i=i, x=x, y=x,
            #                                                   c=color))
        renderer2d.put(pixels)
        self.counter += 1

