
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
                 led_num=DEFAULT_LED_NUM,
                 led_cfg=DEFAULT_LED_CFG):
        self.host = host
        self.port = port
        self.led_num = led_num
        self.led_cfg = led_cfg

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


def renderer_from_args():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--port', type=int, default=7890)
    parser.add_argument('--host', default='localhost')
    parser.add_argument('-n', '--led-num', type=int, default=64)
    parser.add_argument('-c', '--led-cfg', default=None)
    args = parser.parse_args()
    return Renderer(host=args.host, port=args.port, led_num=args.led_num,
                    led_cfg=args.led_cfg)


