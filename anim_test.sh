#!/bin/bash

export LED_MAPPING="$(pwd)/configs/floasis_2d_8x8.tsv"
export FADECANDY_HOST="localhost"
#export FADECANDY_HOST="raspberrypi0.local"

PYTHONPATH=$(pwd) python3 $(pwd)/lib/floasis/main.py \
    --led-cfg=${LED_MAPPING} \
    --led-num=64 \
    --width=8 \
    --height=7 \
    --tick=0.2 \
    --host=${FADECANDY_HOST}
