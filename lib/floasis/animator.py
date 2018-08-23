#!/usr/bin/env python

import time
import numpy as np

from lib.floasis.input_handler import InputHandler
from lib.floasis.render import renderer2d_argparser, renderer2d_from_args


DEFAULT_SCALE_0 = 0.2
DEFAULT_SCALE_1 = 0.4
DEFAULT_SCALE_2 = 0.8
DEFAULT_SPEED_COEF = 1.0

MAX_SPEED_COEF = 4.0
MIN_SPEED_COEF = 0.4

MAX_SCALE = 2.0
MIN_SCALE = 2.0
SCALE_STEP_SIZE = 0.2


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


DEFAULT_ANIMATION_FUNC = cosine
ANIMATIONS = {
    'cosine': cosine,
}


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
        self.anim_name = 'cosine'

    def anim_func(self):
        """ get the current animation function safely - if anything is
        misconfigured, use a default animation function. """
        return ANIMATIONS.get(self.anim_name, DEFAULT_ANIMATION_FUNC)

    def update_speed_coef(self, newval):
        sigmoided = 1 / (1 + np.exp(-newval))
        self.speed_coef = MIN_SPEED_COEF + (sigmoided * MAX_SPEED_COEF)

    def update_scale_0(self):
        if self.scale_0_order == 'UP' and self.scale_0 >= MAX_SCALE:
            self.scale_0_order = 'DOWN'
        elif self.scale_0_order == 'DOWN' and self.scale_0 <= MIN_SCALE:
            self.scale_0_order = 'UP'

        sign = 1.0 if self.scale_0_order == 'UP' else -1.0
        delta = sign * SCALE_STEP_SIZE
        self.scale_0_order += delta

    def draw(self):
        # get the current animation function
        xy_func = self.anim_func()

        pixels = [(0, 0, 0)] * renderer2d.led_num
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


if __name__ == '__main__':
    parser = renderer2d_argparser()
    args = parser.parse_args()
    renderer2d = renderer2d_from_args(args)
    renderer2d.load_cfg()

    anim = Animator(_renderer=renderer2d)
    input_handler = InputHandler(
        rotary_callback=anim.update_speed_coef,
        up_callback=anim.update_scale_0,
    )

    while True:
        input_handler.check_input_changes()

        anim.draw()

        time.sleep(0.2)

