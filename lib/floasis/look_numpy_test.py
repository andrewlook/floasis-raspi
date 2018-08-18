from lib.fadecandy.core import opc
import time

ADDRESS = 'localhost:7890'


# Create a client object
client = opc.Client(ADDRESS)

# Test if it can connect (optional)
if client.can_connect():
    print('connected to %s' % ADDRESS)
else:
    # We could exit here, but instead let's just print a warning
    # and then keep trying to send pixels in case the server
    # appears later
    print('WARNING: could not connect to %s' % ADDRESS)

# Send pixels forever at 30 frames per second
while True:
    my_pixels = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    if client.put_pixels(my_pixels, channel=0):
        print('...')
    else:
        print('not connected')
    time.sleep(1/30.0)

import numpy as np


def init_pixels():
    linspace = np.linspace(0, 2*np.pi, 64)
    sine_wave = np.sin(linspace)
    abs_sine = np.abs(sine_wave)
    nums = [int(i) for i in (abs_sine * 256)]
    pixels = [(j, j, j) for j in nums]
    return pixels


def do_the_wave():
    pixels = init_pixels()
    # Send pixels forever at 30 frames per second
    while True:
        if client.put_pixels(pixels, channel=0):
            pass
            # print('...')
        else:
            print('not connected')
        time.sleep(1/30.0)
        pixels = pixels[-1:] + pixels[:-1]


def blackout():
    zeros = [(0, 0, 0)] * 64
    client.put_pixels(zeros, channel=0)
