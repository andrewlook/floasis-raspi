#!/usr/bin/env python

from lib.floasis.render import argparser, renderer_from_args


def measuring_stick(num_leds=64):
    string = [ (128, 128, 128) ] * num_leds
    for i in range(num_leds / 10):
        string[10 * i] = (128, 255, 128)
    return string


if __name__ == '__main__':
    parser = argparser()
    args = parser.parse_args()
    renderer = renderer_from_args(args)

    pixels = measuring_stick(renderer.led_num)
    pixels = measuring_stick(renderer.led_num)

    renderer.put(pixels)