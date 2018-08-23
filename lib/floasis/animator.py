#!/usr/bin/env python

import logging
import time
import numpy as np

from lib.floasis.render import renderer2d_argparser, renderer2d_from_args
from lib.floasis.config import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def color256(decimal_num):
    """ convert a floating point number in the range (-1.0, 1.0) to
        an int in the range (0, 256)
    """
    return int(decimal_num * 128) + 128


class Animator(object):

    def __init__(self,
                 _renderer,
                 scale_0_mgr=None,
                 scale_1_mgr=None,
                 speed_coef_mgr=None):
        self.renderer = _renderer

        self.scale_0_mgr = scale_0_mgr
        self.scale_1_mgr = scale_1_mgr
        self.speed_coef_mgr = speed_coef_mgr

        # time step - makes the animation move
        self.counter = 0

        # which animation to do
        self.anim_num = 1
        
        self._DEFAULT_ANIMATION_FUNC = cosine
        self._ANIMATIONS = {
            'cosine': self.cosine,
            'circle': self.circle,
        }
        self._ALL_ANIMS = list(self._ANIMATIONS.keys())
        self._NUM_ANIMS = len(self._ALL_ANIMS)

    @property
    def speed_coef(self):
        return self.speed_coef_mgr.val

    @property
    def scale_0(self):
        return self.scale_0_mgr.val

    @property
    def scale_1(self):
        return self.scale_1_mgr.val

    # TODO(look) replace this with the button handler
    def anim_func(self):
        """ get the current animation function safely - if anything is
        misconfigured, use a default animation function. """
        return self._ANIMATIONS.get(self.anim_name, self._DEFAULT_ANIMATION_FUNC)

    # TODO(look) replace this with the button handler
    @property
    def anim_name(self):
        return self._ALL_ANIMS[self.anim_num]

    # TODO(look) replace this with the button handler
    def next_anim(self):
        old_anim = self.anim_num
        self.anim_num = (self.anim_num + 1) % self._NUM_ANIMS
        new_anim = self.anim_name
        print('{o} -> {n}'.format(o=old_anim, n=new_anim))

    def draw(self):
        # get the current animation function
        xy_func = self.anim_func()

        # TODO(look): i vs. ordinal position for missing pixels?
        for i, coord in enumerate(self.renderer.ord_to_xy):
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
            self.pixels[i] = color

            # print('i = {i}   ( x = {x}, y = {y} )  {c}'.format(i=i, x=x, y=x,
            #                                                   c=color))
        self.renderer.put(self.pixels)
        self.counter += 1

    def cosine(self, x, y, cnt):
        t = (speed_coef * cnt)
        red = np.cos(self.scale_0 * x + t)
        green = np.sin(self.scale_1 * y + t)
        blue = np.sin((self.scale_0 + self.scale_1) * x + y + t)

        return color256(red), color256(green), color256(blue)

    def circle(self, x, y, cnt):
        rad = np.sqrt(((1.0 * (self.scale_0 - x)) ** 2) + ((1.0 * (self.scale_1 - y)) ** 2))
        t = (self.speed_coef * cnt)
        retval = (
            color256(np.sin(4.0 * (rad + t))),
            color256(np.cos(1.0 * (2 * rad + t))),
            color256(np.cos(2.0 * (rad + t))),
        )
        return retval

    def old_circle(self, x, y, cnt):
        rad = np.sqrt(((1.0 * x) ** 2) + ((1.0 * y) ** 2))
        t = (self.speed_coef * cnt)
        retval = (
            color256(np.sin(self.scale_0 * (rad + t))),
            color256(np.cos(self.scale_1 * (2 * rad + t))),
            color256(np.cos((self.scale_0 + self.scale_1) * (rad + t))),
        )
        return retval



