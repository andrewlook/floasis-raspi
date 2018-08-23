#!/bin/bash

export LED_MAPPING="$(pwd)/configs/floasis_2d_8x8.tsv"
export FADECANDY_HOST="raspberrypi1.local"

PYTHONPATH=$(pwd) python3 $(pwd)/lib/floasis/animator.py \
    --led-cfg=${LED_MAPPING} \
    --host=${FADECANDY_HOST}
