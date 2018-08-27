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