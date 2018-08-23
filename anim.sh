#!/bin/bash

export LED_MAPPING="$(pwd)/configs/full.tsv"
export FADECANDY_HOST="raspberrypi0.local"

PYTHONPATH=$(pwd) python3 $(pwd)/lib/floasis/main.py \
    --led-cfg=${LED_MAPPING} \
    --led-num=1024 \
    --width=80 \
    --height=80 \
    --host=${FADECANDY_HOST}
