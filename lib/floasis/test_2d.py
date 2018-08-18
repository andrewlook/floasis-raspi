#!/usr/bin/env python

from lib.floasis.render import renderer2d_argparser, renderer2d_from_args


def xy_func(x, y):
    # if the x/y values in the map were -1, render black for this pixel
    if x < 0 or y < 0:
        return (0, 0, 0)

    retval = (0, 0, 0)
    if y % 2 == 0:
        retval = (128, 128, 128)
    return retval


if __name__ == '__main__':
    parser = renderer2d_argparser()
    args = parser.parse_args()
    renderer2d = renderer2d_from_args(args)

    from pprint import pprint
    pprint(renderer2d.__dict__)

    renderer2d.load_cfg()

    pprint(renderer2d.ord_to_xy)

    renderer2d.apply_xy(xy_func)
