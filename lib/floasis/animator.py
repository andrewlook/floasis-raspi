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
                 speed_coef_mgr=None,
                 buttons=None,
                ):
        self.renderer = _renderer

        self.scale_0_mgr = scale_0_mgr
        self.scale_1_mgr = scale_1_mgr
        self.speed_coef_mgr = speed_coef_mgr
        self.buttons = buttons

        # time step - makes the animation move
        self.counter = 0

        # which animation to do
        self.anim_num = 1
        
        self._DEFAULT_ANIMATION_FUNC = self.cosine
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

        self.red_hold = self.buttons.red_hold
        self.grn_hold = self.buttons.grn_hold
        self.blu_hold = self.buttons.blu_hold
        self.whi_hold = self.buttons.whi_hold

        self.red_press = self.buttons.red_press
        self.grn_press = self.buttons.grn_press
        self.blu_press = self.buttons.blu_press
        self.whi_press = self.buttons.whi_press

        self.red_down = self.buttons.red_down
        self.grn_down = self.buttons.grn_down
        self.blu_down = self.buttons.blu_down
        self.whi_down = self.buttons.whi_down

        t = self.counter * self.speed_coef

        if self.counter % 100:
            print('speed={s} t={t}, s0={s0}, s1={s1}'
                  '\n\trp={rp}, gp={gp}, bp={bp}, wp={wp}'
                  '\n\trh={rh}, gh={gh}, bh={bh}, wh={wh}'
                  '\n\trd={rd}, gd={gd}, bd={bd}, wd={wd}'
                  .format(s=self.speed_coef,
                          t=t,
                          s0=self.scale_0,
                          s1=self.scale_1,
                          rp=self.red_press,
                          gp=self.grn_press,
                          bp=self.blu_press,
                          wp=self.whi_press,
                          rh=self.red_hold,
                          gh=self.grn_hold,
                          bh=self.blu_hold,
                          wh=self.whi_hold,
                          rd=self.red_down,
                          gd=self.grn_down,
                          bd=self.blu_down,
                          wd=self.whi_down,
                         )
                 )

        # TODO(look): i vs. ordinal position for missing pixels?
        for i, coord in enumerate(self.renderer.ord_to_xy):
            x, y = coord
            # if the x/y values in the map were -1, (meaning the config
            # file says to ignore this pixel), render black for this pixel
            if x < 0 or y < 0:
                continue

            color = xy_func(x, y, t=t)
            self.renderer.pixels[i] = color

            # print('i = {i}   ( x = {x}, y = {y} )  {c}'.format(i=i, x=x, y=x,
            #                                                   c=color))
        self.renderer.put(self.renderer.pixels)
        self.counter += 1

    def cosine(self, x, y, t):
        #red = np.cos(self.scale_0 * self.red_hold * (x ** self.scale_1) + t) if self.red_down else 0
        #grn = np.sin(self.scale_0 * self.grn_hold * (y ** self.scale_1) + t) if self.grn_down else 0
        #blu = np.sin(self.scale_0 * self.blu_hold * ((x + y) ** self.scale_1) + t) if self.blu_down else 0
        red = np.cos(self.red_hold * x + t) if self.red_down else 0
        grn = np.sin(self.grn_hold * y + t) if self.grn_down else 0
        blu = np.sin(self.blu_hold * (x + y) + t) if self.blu_down else 0
        return color256(red), color256(grn), color256(blu)

    def circle(self, x, y, t):
        rad = np.sqrt(((1.0 * (self.scale_0 - x)) ** 2) + ((1.0 * (self.scale_1 - y)) ** 2))
        retval = (
            #color256(np.sin(self.red_hold * (rad + t)) if self.red_down else 0),
            #color256(np.cos(self.grn_hold * (2 * rad + t)) if self.grn_down else 0),
            #color256(np.cos(self.blu_hold * (rad + t)) if self.blu_down else 0),
            color256(np.sin(self.red_hold * (rad + t)) if self.red_down else 0),
            color256(np.cos(self.grn_hold * (rad + t)) if self.grn_down else 0),
            color256(np.cos(self.blu_hold * (rad + t)) if self.blu_down else 0),
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



