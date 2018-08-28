#!/usr/bin/env python

from pprint import pprint
from lib.floasis.render import renderer2d_argparser, renderer2d_from_args


def xy_func(x, y):
    retval = (0, 0, 0)
    if y % 2 == 0:
        retval = (128, 128, 128)
    else:
        retval = (128, 0, 0)
    return retval


if __name__ == '__main__':
    parser = renderer2d_argparser()
    args = parser.parse_args()
    renderer2d = renderer2d_from_args(args)
    renderer2d.load_cfg()

    pixels = [(0, 0, 0)] * renderer2d.led_num
    for i, coord in enumerate(renderer2d.ord_to_xy):
        x, y = coord
        # if the x/y values in the map were -1, render black for this pixel
        if x < 0 or y < 0:
            continue

        color = xy_func(x, y)
        pixels[i] = color

        print('i = {i}   ( x = {x}, y = {y} )  {c}'.format(i=i, x=x, y=x,
                                                           c=color))
    renderer2d.put(pixels)

