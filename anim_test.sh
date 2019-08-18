#!/bin/bash

PYTHONPATH=$(pwd) python3 $(pwd)/lib/floasis/main.py \
    --led-cfg="$(pwd)/configs/flo_tsv/floasis_2d_8x8.tsv" \
    --led-num=64 \
    --width=8 \
    --height=7 \
    --tick=0.2 \
    --host=localhost
