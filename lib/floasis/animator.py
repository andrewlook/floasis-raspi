#!/usr/bin/env python

import logging
import time
import numpy as np

from lib.floasis.input_handler import InputHandler
from lib.floasis.render import renderer2d_argparser, renderer2d_from_args
from lib.floasis.config import *
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def color256(decimal_num):
    """ convert a floating point number in the range (-1.0, 1.0) to
        an int in the range (0, 256)
    """
    return int(decimal_num * 128) + 128


def cosine(x, y, cnt, **kwargs):

    scale_0 = kwargs.get('scale_0', DEFAULT_SCALE_0)
    scale_1 = kwargs.get('scale_1', DEFAULT_SCALE_1)
    scale_2 = kwargs.get('scale_2', DEFAULT_SCALE_2)
    speed_coef = kwargs.get('speed_coef', DEFAULT_SPEED_COEF)

    t = (speed_coef * cnt)
    red = np.cos(scale_0 * x + t)
    green = np.sin(scale_1 * y + t)
    blue = np.sin(scale_2 * x + y + t)

    return color256(red), color256(green), color256(blue)


def circle(x, y, cnt, **kwargs):
    scale_0 = kwargs.get('scale_0', DEFAULT_SCALE_0)
    scale_1 = kwargs.get('scale_1', DEFAULT_SCALE_1)
    scale_2 = kwargs.get('scale_2', DEFAULT_SCALE_2)
    speed_coef = kwargs.get('speed_coef', DEFAULT_SPEED_COEF)

    rad = np.sqrt(((1.0 * x) ** 2) + ((1.0 * y) ** 2))
    t = (speed_coef * cnt)
    retval = (
        color256(np.sin(scale_0 * (rad + t))),
        color256(np.cos(scale_1 * (2 * rad + t))),
        color256(np.cos(scale_2 * (rad + t))),
    )
    return retval


DEFAULT_ANIMATION_FUNC = cosine
ANIMATIONS = {
    'cosine': cosine,
    'circle': circle,
}
ALL_ANIMS = list(ANIMATIONS.keys())
NUM_ANIMS = len(ALL_ANIMS)


class Animator(object):

    def __init__(self, _renderer):
        self.renderer = _renderer

        # time step - makes the animation move
        self.counter = 0

        # variables controlled by inputs, shared across animations
        self.scale_0 = DEFAULT_SCALE_0
        self.scale_0_order = 'UP'
        self.scale_1 = DEFAULT_SCALE_1
        self.scale_1_order = 'UP'
        self.scale_2 = DEFAULT_SCALE_2
        self.scale_2_order = 'UP'
        self.speed_coef = DEFAULT_SPEED_COEF

        # which animation to do
        self.anim_num = 0

    def anim_func(self):
        """ get the current animation function safely - if anything is
        misconfigured, use a default animation function. """
        return ANIMATIONS.get(self.anim_name, DEFAULT_ANIMATION_FUNC)

    @property
    def anim_name(self):
        return ALL_ANIMS[self.anim_num]

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

    def update_scale_0(self):
        if self.scale_0_order == 'UP' and self.scale_0 >= MAX_SCALE:
            self.scale_0_order = 'DOWN'
        elif self.scale_0_order == 'DOWN' and self.scale_0 <= MIN_SCALE:
            self.scale_0_order = 'UP'

        sign = 1.0 if self.scale_0_order == 'UP' else -1.0
        delta = sign * SCALE_STEP_SIZE
        self.scale_0 += delta
        print('scale_0 = {s}, order = {o}'.format(s=self.scale_0,
                                                        o=self.scale_0_order))

    def update_scale_1(self):
        if self.scale_1_order == 'UP' and self.scale_1 >= MAX_SCALE:
            self.scale_1_order = 'DOWN'
        elif self.scale_1_order == 'DOWN' and self.scale_1 <= MIN_SCALE:
            self.scale_1_order = 'UP'

        sign = 1.0 if self.scale_1_order == 'UP' else -1.0
        delta = sign * SCALE_STEP_SIZE
        self.scale_1 += delta
        print('scale_1 = {s}, order = {o}'.format(s=self.scale_1,
                                                        o=self.scale_1_order))

    def update_scale_2(self):
        if self.scale_2_order == 'UP' and self.scale_2 >= MAX_SCALE:
            self.scale_2_order = 'DOWN'
        elif self.scale_2_order == 'DOWN' and self.scale_2 <= MIN_SCALE:
            self.scale_2_order = 'UP'

        sign = 1.0 if self.scale_2_order == 'UP' else -1.0
        delta = sign * SCALE_STEP_SIZE
        self.scale_2 += delta
        print('scale_2 = {s}, order = {o}'.format(s=self.scale_2,
                                                  o=self.scale_2_order))

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
                            scale_2=self.scale_2,
                            speed_coef=self.speed_coef)
            pixels[i] = color

            # print('i = {i}   ( x = {x}, y = {y} )  {c}'.format(i=i, x=x, y=x,
            #                                                   c=color))
        renderer2d.put(pixels)
        self.counter += 1

