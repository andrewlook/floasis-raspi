import os
import time
import numpy as np

from lib.fadecandy.core import opc

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = '7890'
DEFAULT_LED_NUM = 64
DEFAULT_LED_CFG = None


class Renderer(object):

    def __init__(self,
                 host=DEFAULT_HOST,
                 port=DEFAULT_PORT,
                 led_num=DEFAULT_LED_NUM):
        self.host = host
        self.port = port
        self.led_num = led_num

        self.address = '{host}:{port}'.format(host=host, port=port)
        # Create a client object
        self.client = opc.Client(self.address)

        # Test if it can connect (optional)
        if self.client.can_connect():
            print('connected to %s' % self.address)
        else:
            # We could exit here, but instead let's just print a warning
            # and then keep trying to send pixels in case the server
            # appears later
            raise Exception('WARNING: could not connect to %s' % self.address)

    def put(self, _pixels):
        self.client.put_pixels(_pixels, channel=0)


class Renderer2D(Renderer):

    def __init__(self,
                 led_cfg=DEFAULT_LED_CFG,
                 width=8,
                 height=8,
                 **kwargs):
        super(Renderer2D, self).__init__(**kwargs)
        self.width = width,
        self.height = height
        self.led_cfg = led_cfg
        self.xy_to_ord = None
        self.ord_to_xy = None

    def _read_cfg(self, fname):
        """ file format for TSV:
                x   y   LED_position
        """
        if not os.path.exists(fname):
            raise Exception('file doesnt exist: ' + fname)

        with open(fname) as fd:
            lines = fd.readlines()
            rows = [s.strip().split('\t') for s in lines]
            if len(rows) > self.led_num:
                raise Exception('num csv rows ({c}) greater than num LEDs {n}'
                                .format(c=len(rows), n=self.led_num))
            coords = [(int(r[0]), int(r[1]), int(r[2])) for r in rows]
        return coords

    def load_cfg(self):
        coords = self._read_cfg(self.led_cfg)
        self.xy_to_ord = [[-1] * self.width] * self.height
        self.ord_to_xy = [(-1, -1)] * self.led_num

        for x, y, ord in coords:
            self.mapping[x][y] = ord
            self.ord_to_xy[ord] = (x, y)

    def apply_xy(self, func, *args, **kwargs):
        """ func should take x,y and return a color (R, G, B) """
        if not self.ord_to_xy:
            raise Exception('self.ord_to_xy is missing, run load_cfg first!')

        pixels = [func(x=r[0], y=r[1], *args, **kwargs)
                  for r in self.ord_to_xy]
        self.put(pixels)


def renderer_argparser():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--port', type=int, default=7890)
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--led-num', type=int, default=64)
    return parser


def renderer_from_args(args):
    return Renderer(host=args.host, port=args.port, led_num=args.led_num)


def renderer2d_argparser():
    parser = renderer_argparser()
    parser.add_argument('--width', type=int, default=8)
    parser.add_argument('--height', type=int, default=8)
    parser.add_argument('--led-cfg', default=None)
    return parser


def renderer2d_from_args(args):
    print(args)
    return Renderer2D(
        host=args.host,
        port=args.port,
        led_num=args.led_num,
        width=args.width,
        height=args.height,
        led_cfg=args.led_cfg
    )
