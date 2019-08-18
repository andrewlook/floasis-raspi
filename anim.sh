#!/bin/bash

PYTHONPATH=$(pwd) python3 $(pwd)/lib/floasis/main.py \
    --led-cfg="$(pwd)/configs/flo_tsv/full.tsv" \
    --led-num=1024 \
    --width=80 \
    --height=10 \
    --tick=0.2 \
    --host=localhost
