#!/usr/bin/env python

from lib.floasis.render import renderer_argparser, renderer_from_args

red = 0
green = 1
blue = 2

def measuring_stick(start=0, num=50, num_leds=50):
    string = [ (0, 0, 0) ] * num_leds
    for i in range(num):
        rgb = (128, 128, 128)
        mod = i % 5
        if mod == 0:
            rgb = (128, 0, 0)
        elif mod == 1:
            rgb = (0, 128, 0)
        elif mod == 2:
            rgb = (0, 0, 128)
        elif mod == 3:
            rgb = (128, 128, 0)
        elif mod == 4:
            rgb = (0, 128, 128)
        else:
            raise Exception('wtf')
        string[start + i] = rgb
    print(string)
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

