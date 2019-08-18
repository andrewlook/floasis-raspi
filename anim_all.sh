#!/bin/bash

PYTHONPATH=$(pwd) python3 $(pwd)/lib/floasis/main.py \
    --led-cfg="$(pwd)/configs/flo_tsv/all.tsv" \
    --led-num=1024 \
    --width=50 \
    --height=16 \
    --tick=0.2 \
    --host=localhost
