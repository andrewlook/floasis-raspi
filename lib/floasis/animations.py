import numpy as np

from lib.floasis.config import *

def color256(decimal_num):
    """ convert a floating point number in the range (-1.0, 1.0) to
        an int in the range (0, 256)
    """
    return int(decimal_num * 128) + 128


def cosine(x, y, cnt, **kwargs):

    scale_0 = kwargs.get('scale_0', DEFAULT_SCALE_0)
    scale_1 = kwargs.get('scale_1', DEFAULT_SCALE_1)
    scale_2 = kwargs.get('scale_2', DEFAULT_SCALE_2)
    speed_coef = kwargs.get('speed_coef', DEFAULT_SPEED_COEF)

    t = (speed_coef * cnt)
    red = np.cos(scale_0 * x + t)
    green = np.sin(scale_1 * y + t)
    blue = np.sin(scale_2 * x + y + t)

    return color256(red), color256(green), color256(blue)


def circle(x, y, cnt, **kwargs):
    scale_0 = kwargs.get('scale_0', DEFAULT_SCALE_0)
    scale_1 = kwargs.get('scale_1', DEFAULT_SCALE_1)
    scale_2 = kwargs.get('scale_2', DEFAULT_SCALE_2)
    speed_coef = kwargs.get('speed_coef', DEFAULT_SPEED_COEF)

    rad = np.sqrt(((1.0 * x) ** 2) + ((1.0 * y) ** 2))
    t = (speed_coef * cnt)
    retval = (
        color256(np.sin(scale_0 * (rad + t))),
        color256(np.cos(scale_1 * (2 * rad + t))),
        color256(np.cos(scale_2 * (rad + t))),
    )
    return retval


DEFAULT_ANIMATION_FUNC = cosine
ANIMATIONS = {
    'cosine': cosine,
    'circle': circle,
}
ALL_ANIMS = list(ANIMATIONS.keys())
NUM_ANIMS = len(ALL_ANIMS)


