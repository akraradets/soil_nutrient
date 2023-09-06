#!/bin/bash

python3 linearplot.py --image_set om --model_name alexnet --device all --environment indoor  --clip_target True --normalize_target True --epochs 50 --lr 0.001
python3 linearplot.py --image_set om --model_name alexnet --device all --environment outdoor --clip_target True --normalize_target True --epochs 50 --lr 0.001

python3 linearplot.py --image_set p --model_name alexnet --device all --environment indoor  --clip_target True --normalize_target True --epochs 50 --lr 0.001
python3 linearplot.py --image_set p --model_name alexnet --device all --environment outdoor --clip_target True --normalize_target True --epochs 50 --lr 0.001

# python3 linearplot.py --image_set k --model_name alexnet --device all --environment indoor  --clip_target True --normalize_target True --epochs 50 --lr 0.001
# python3 linearplot.py --image_set k --model_name alexnet --device all --environment outdoor --clip_target True --normalize_target True --epochs 50 --lr 0.001