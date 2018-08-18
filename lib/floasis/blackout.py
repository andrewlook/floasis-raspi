#!/usr/bin/env python

# Light each LED in sequence, and repeat.

from lib.fadecandy.core import opc
import time

numLEDs = 30
client = opc.Client('localhost:7890')
pixels = [ (0,0,0) ] * numLEDs
client.put_pixels(pixels)
