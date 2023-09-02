#!/bin/bash

python3 train_bigset.py --image_set om --model_name alexnet   --device all --environment all --clip_target True --normalize_target True --epochs 200 --lr 0.001
python3 train_bigset.py --image_set om --model_name resnet    --device all --environment all --clip_target True --normalize_target True --epochs 200 --lr 0.001
python3 train_bigset.py --image_set om --model_name mobilenet --device all --environment all --clip_target True --normalize_target True --epochs 200 --lr 0.001

python3 train_bigset.py --image_set p --model_name alexnet   --device all --environment all --clip_target True --normalize_target True --epochs 200 --lr 0.001
python3 train_bigset.py --image_set p --model_name resnet    --device all --environment all --clip_target True --normalize_target True --epochs 200 --lr 0.001
python3 train_bigset.py --image_set p --model_name mobilenet --device all --environment all --clip_target True --normalize_target True --epochs 200 --lr 0.001

python3 train_bigset.py --image_set k --model_name alexnet   --device all --environment all --clip_target True --normalize_target True --epochs 200 --lr 0.001
python3 train_bigset.py --image_set k --model_name resnet    --device all --environment all --clip_target True --normalize_target True --epochs 200 --lr 0.001
python3 train_bigset.py --image_set k --model_name mobilenet --device all --environment all --clip_target True --normalize_target True --epochs 200 --lr 0.001