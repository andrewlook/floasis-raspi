#!/usr/bin/env python

import time
from lib.floasis.render import argparser, renderer_from_args


def chaser(i, num_leds=64):
	dots = [(0, 0, 0)] * num_leds
	dots[i] = (128, 128, 128)
	return dots


if __name__ == '__main__':
	parser = argparser()
	args = parser.parse_args()
	renderer = renderer_from_args(args)

	while True:
		for i in range(renderer.led_num):
			pixels = chaser(i, num_leds=renderer.led_num)
			renderer.put(pixels)
			time.sleep(0.05)

