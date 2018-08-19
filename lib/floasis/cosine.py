#!/usr/bin/env python

import time
import numpy as np
from pprint import pprint
from lib.floasis.render import renderer2d_argparser, renderer2d_from_args


def xy_func(x, y, cnt):
    retval = (0, 0, 0)

    c = np.cos(1.0 * x + cnt) # % 8.0)
    c256 = int(c * 128) + 128
    
    c2 = np.sin(2.0 * y + cnt) # % 9.0)
    c2_256 = int(c2 * 128) + 128
    
    c3 = np.sin(1.0 * x + y + cnt) # % 10.0)
    c3_256 = int(c3 * 128) + 128
    
    print('{c} / {c256}'.format(c=c, c256=c256))
    retval = (c256, c2_256, c3_256)
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

