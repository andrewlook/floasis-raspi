#!/usr/bin/env python

from lib.floasis.render import renderer2d_argparser, renderer2d_from_args


def xy_func(x, y):
    retval = (0, 0, 0)
    if y % 2 == 0:
        retval = (128, 128, 128)
    return retval


if __name__ == '__main__':
    parser = renderer2d_argparser()
    args = parser.parse_args()
    renderer2d = renderer2d_from_args(args)

    renderer2d.apply_xy(xy_func)
