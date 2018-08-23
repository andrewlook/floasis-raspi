#!/usr/bin/env python

from lib.floasis.render import renderer_argparser, renderer_from_args

red = 0
green = 1
blue = 2

def measuring_stick(num_leds=64):
    string = [ (0, 0, 0) ] * num_leds
    for i in range(num_leds / 50):
        color = i % 3
        rgb = [0, 0, 0]
        rgb[color] = 50
        print(rgb)
        for j in range(0, 50):
            step = j % 5
            print(step)
            rgb[color] *= step
            print(rgb)
            string[i + j] = rgb
    print(string)
    return string


if __name__ == '__main__':
    parser = renderer_argparser()
    args = parser.parse_args()
    renderer = renderer_from_args(args)

    pixels = measuring_stick(renderer.led_num)
    pixels = measuring_stick(renderer.led_num)

    renderer.put(pixels)
