#!/usr/bin/env python

import time
import numpy as np
from pprint import pprint
from lib.floasis.render import renderer2d_argparser, renderer2d_from_args


class CPPN(object):

    def __init__(self,
                 num_hidden_layers=3,
                 hidden_layer_size=4,
                 activation='tanh',
                 num_latent=1):
        self.num_hidden_layers = num_hidden_layers
        self.hidden_layer_size = hidden_layer_size
        self.activation = activation
        self.num_latent = num_latent
        self.input_dim = 3 + self.num_latent    # X, Y, R [, z0, ... ]
        self.output_dim = 3                     # R, G, B

        self.input_layer = None
        self.hidden_layers = []
        self.output_layer = None

    def build_model(self):
        dim_input = (self.input_dim, self.hidden_layer_size)
        dim_hidden = (self.hidden_layer_size, self.hidden_layer_size)
        dim_output = (self.hidden_layer_size, self.output_dim)

        self.input_layer = np.random.normal(size=dim_input,
                                            loc=0.0, scale=1.0)
        self.hidden_layers = \
            [np.random.normal(size=(dim_hidden), loc=0.0, scale=1.0)
             for i in range(self.num_hidden_layers)]
        self.output_layer = np.random.normal(size=dim_output,
                                             loc=0.0, scale=1.0)

    def apply_model(self, batch):
        print('batch.shape: ', batch.shape)
        print('input_layer.shape: ', self.input_layer.shape)
        print('output_layer.shape: ', self.output_layer.shape)

        H = np.tanh(np.matmul(batch, self.input_layer))

        print('H[input].shape: ', H.shape)

        for num, hidden_layer in enumerate(self.hidden_layers):
            H = np.tanh(np.matmul(H, hidden_layer))
            print('H[%d].shape: ', (num, H.shape))

        H = np.matmul(H, self.output_layer)
        H = 1/(1+np.exp(-H))  # Sigmoid
        print('H[output].shape: ', H.shape)
        return H

    def normalize_coords(self, coords, width, height):
        normalized = [(
            1.0 * (x / 2) + (1.0 * width / 2),          # centered X
            1.0 * (y / 2) + (1.0 * height / 2),         # centered Y
            np.sqrt(
                (1.0 * 1.0 * (x / 2) + (1.0 * width / 2)) ** 2
                + (1.0 * 1.0 * (y / 2) + (1.0 * height / 2)) ** 2
            ),   # radial distance
        ) for x, y in coords]
        return np.asarray(normalized)


def xy_func(x, y, cnt):
    modded = cnt % 8
    retval = (0, 0, 0)
    if x == modded:
        retval = (128, 128, 128)
    return retval


if __name__ == '__main__':
    parser = renderer2d_argparser()
    parser.add_argument('--num-layers', default=3)
    parser.add_argument('--activation', default='tanh')
    args = parser.parse_args()
    renderer2d = renderer2d_from_args(args)
    renderer2d.load_cfg()

    cppn = CPPN(num_latent=2)
    cppn.build_model()

    counter = 0
    counter_scale = 100

    while True:
        counter += 1
        modcount = counter % counter_scale

        pixels = [(0, 0, 0)] * renderer2d.led_num
        norm_coords = cppn.normalize_coords(coords=renderer2d.ord_to_xy,
                                            width=renderer2d.width,
                                            height=renderer2d.height)
        batch_sz = len(renderer2d.ord_to_xy)
        latent_vec = np.asarray([np.sin(modcount)] * batch_sz,
                                dtype=np.float32).reshape((batch_sz, 1))
        latent_vec2 = np.asarray([np.cos(counter % 20)] * batch_sz,
                                dtype=np.float32).reshape((batch_sz, 1))
        print('norm_coords.shape: ', norm_coords.shape)
        print('latent_vec.shape: ', latent_vec.shape)
        with_latent = np.hstack([
            norm_coords,
            latent_vec,
            latent_vec2,
        ])
        print('with_latent.shape: ', with_latent.shape)

        for i, coord in enumerate(renderer2d.ord_to_xy):
            x, y = coord
            # if the x/y values in the map were -1, render black for this pixel
            if x < 0 or y < 0:
                continue

            color = list(cppn.apply_model(with_latent[i, :]) * 255.0)
            pixels[i] = color

            print('i = {i}   ( x = {x}, y = {y} )  {c}'.format(i=i, x=x, y=x,
                                                               c=color))
        renderer2d.put(pixels)

        time.sleep(0.5)

