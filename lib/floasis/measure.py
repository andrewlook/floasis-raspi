#!/usr/bin/env python

from lib.floasis.render import renderer_from_args


def measuring_stick(num_leds=64):
    string = [ (128, 128, 128) ] * num_leds
    for i in range(num_leds / 10):
        string[10 * i] = (128, 255, 128)
    return string


if __name__ == '__main__':
    renderer = renderer_from_args()

    pixels = measuring_stick(renderer.led_num)
    pixels = measuring_stick(renderer.led_num)

    renderer.put(pixels)
