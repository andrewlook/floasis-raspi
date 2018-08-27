#!/usr/bin/env python

from lib.floasis.render import renderer_argparser, renderer_from_args


def blackout(num_leds=64):
    zeros = [(0, 0, 0)] * num_leds
    return zeros


if __name__ == '__main__':
    parser = renderer_argparser()
    args = parser.parse_args()
    renderer = renderer_from_args(args)

    pixels = blackout(renderer.led_num)

    renderer.put(pixels)
