#!/usr/bin/env python

from lib.floasis.render import renderer_argparser, renderer_from_args

red = 0
green = 1
blue = 2

def measuring_stick(start=0, num=50, num_leds=50):
    string = [ (0, 0, 0) ] * num_leds
    for i in range(num):
        val = 0
        mod = i % 5
        if mod == 0:
            val = 255
        elif mod == 1:
            val = 200
        elif mod == 2:
            val = 150
        elif mod == 3:
            val = 100
        elif mod == 4:
            val = 50
        else:
            raise Exception('wtf')

        quarter = (i / 5) % 4
        if quarter == 0:
            rgb = (val, 0, 0)
        elif quarter == 1:
            rgb = (0, val, 0)
        elif quarter == 2:
            rgb = (0, 0, val)
        elif quarter == 3:
            rgb = (val, val, 0)

        if mod == 4:
            rgb = (128, 128, 128)
        print(start + i)
        string[start + i] = rgb
    return string


if __name__ == '__main__':
    parser = renderer_argparser()
    parser.add_argument('--start', default=0, type=int)
    parser.add_argument('--num', default=50, type=int)
    args = parser.parse_args()
    renderer = renderer_from_args(args)

    pixels = measuring_stick(num_leds=renderer.led_num, start=args.start, num=args.num)
    renderer.put(pixels)
    pixels = measuring_stick(num_leds=renderer.led_num, start=args.start, num=args.num)
    renderer.put(pixels)

