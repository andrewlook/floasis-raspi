#!/usr/bin/env python

import time
import numpy as np
from pprint import pprint
from lib.floasis.render import renderer2d_argparser, renderer2d_from_args


def xy_func(x, y, cnt):
    retval = (0, 0, 0)

    r = np.sqrt(((1.0 * x) ** 2) + ((1.0 * y) ** 2))

    retval = (
            int(np.sin(0.2 * (r + cnt)) * 128) + 128,
            int(np.cos(1.6 * (2 * r + cnt)) * 128) + 128,
            int(np.cos(0.8 * (r + cnt)) * 128) + 128,
            )
    return retval


if __name__ == '__main__':
    parser = renderer2d_argparser()
    args = parser.parse_args()
    renderer2d = renderer2d_from_args(args)
    renderer2d.load_cfg()

    counter = 0

    while True:
        pixels = [(0, 0, 0)] * renderer2d.led_num
        for i, coord in enumerate(renderer2d.ord_to_xy):
            x, y = coord
            # if the x/y values in the map were -1, render black for this pixel
            if x < 0 or y < 0:
                continue

            color = xy_func(x, y, cnt=counter)
            pixels[i] = color

            print('i = {i}   ( x = {x}, y = {y} )  {c}'.format(i=i, x=x, y=x,
                                                               c=color))
        renderer2d.put(pixels)
        counter += 1
        time.sleep(0.2)

