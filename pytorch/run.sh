#!/bin/bash

python3 train_bigset.py --image_set om --model_name alexnet --device iphone --environment all  --clip_target True --normalize_target True --epochs 50 --lr 0.001
python3 linearplot.py   --image_set om --model_name alexnet --device iphone --environment all  --clip_target True --normalize_target True
python3 train_bigset.py --image_set om --model_name alexnet --device samsung --environment all --clip_target True --normalize_target True --epochs 50 --lr 0.001
python3 linearplot.py   --image_set om --model_name alexnet --device samsung --environment all --clip_target True --normalize_target True
python3 train_bigset.py --image_set om --model_name alexnet --device redmi --environment all   --clip_target True --normalize_target True --epochs 50 --lr 0.001
python3 linearplot.py   --image_set om --model_name alexnet --device redmi --environment all   --clip_target True --normalize_target True
python3 train_bigset.py --image_set om --model_name alexnet --device oppo --environment all   --clip_target True --normalize_target True --epochs 50 --lr 0.001
python3 linearplot.py   --image_set om --model_name alexnet --device oppo --environment all   --clip_target True --normalize_target True
python3 train_bigset.py --image_set om --model_name alexnet --device iphone --environment indoor  --clip_target True --normalize_target True --epochs 50 --lr 0.001
python3 linearplot.py   --image_set om --model_name alexnet --device iphone --environment indoor  --clip_target True --normalize_target True
python3 train_bigset.py --image_set om --model_name alexnet --device samsung --environment indoor --clip_target True --normalize_target True --epochs 50 --lr 0.001
python3 linearplot.py   --image_set om --model_name alexnet --device samsung --environment indoor --clip_target True --normalize_target True
python3 train_bigset.py --image_set om --model_name alexnet --device redmi --environment indoor   --clip_target True --normalize_target True --epochs 50 --lr 0.001
python3 linearplot.py   --image_set om --model_name alexnet --device redmi --environment indoor   --clip_target True --normalize_target True
python3 train_bigset.py --image_set om --model_name alexnet --device oppo --environment indoor   --clip_target True --normalize_target True --epochs 50 --lr 0.001
python3 linearplot.py   --image_set om --model_name alexnet --device oppo --environment indoor   --clip_target True --normalize_target True
python3 train_bigset.py --image_set om --model_name alexnet --device iphone --environment outdoor  --clip_target True --normalize_target True --epochs 50 --lr 0.001
python3 linearplot.py   --image_set om --model_name alexnet --device iphone --environment outdoor  --clip_target True --normalize_target True
python3 train_bigset.py --image_set om --model_name alexnet --device samsung --environment outdoor --clip_target True --normalize_target True --epochs 50 --lr 0.001
python3 linearplot.py   --image_set om --model_name alexnet --device samsung --environment outdoor --clip_target True --normalize_target True
python3 train_bigset.py --image_set om --model_name alexnet --device redmi --environment outdoor   --clip_target True --normalize_target True --epochs 50 --lr 0.001
python3 linearplot.py   --image_set om --model_name alexnet --device redmi --environment outdoor   --clip_target True --normalize_target True
python3 train_bigset.py --image_set om --model_name alexnet --device oppo --environment outdoor   --clip_target True --normalize_target True --epochs 50 --lr 0.001
python3 linearplot.py   --image_set om --model_name alexnet --device oppo --environment outdoor   --clip_target True --normalize_target True

python3 train_bigset.py --image_set p --model_name alexnet --device iphone --environment all  --clip_target True --normalize_target True --epochs 50 --lr 0.001
python3 linearplot.py   --image_set p --model_name alexnet --device iphone --environment all  --clip_target True --normalize_target True
python3 train_bigset.py --image_set p --model_name alexnet --device samsung --environment all --clip_target True --normalize_target True --epochs 50 --lr 0.001
python3 linearplot.py   --image_set p --model_name alexnet --device samsung --environment all --clip_target True --normalize_target True
python3 train_bigset.py --image_set p --model_name alexnet --device redmi --environment all   --clip_target True --normalize_target True --epochs 50 --lr 0.001
python3 linearplot.py   --image_set p --model_name alexnet --device redmi --environment all   --clip_target True --normalize_target True
python3 train_bigset.py --image_set p --model_name alexnet --device iphone --environment indoor  --clip_target True --normalize_target True --epochs 50 --lr 0.001
python3 linearplot.py   --image_set p --model_name alexnet --device iphone --environment indoor  --clip_target True --normalize_target True
python3 train_bigset.py --image_set p --model_name alexnet --device samsung --environment indoor --clip_target True --normalize_target True --epochs 50 --lr 0.001
python3 linearplot.py   --image_set p --model_name alexnet --device samsung --environment indoor --clip_target True --normalize_target True
python3 train_bigset.py --image_set p --model_name alexnet --device redmi --environment indoor   --clip_target True --normalize_target True --epochs 50 --lr 0.001
python3 linearplot.py   --image_set p --model_name alexnet --device redmi --environment indoor   --clip_target True --normalize_target True
python3 train_bigset.py --image_set p --model_name alexnet --device iphone --environment outdoor  --clip_target True --normalize_target True --epochs 50 --lr 0.001
python3 linearplot.py   --image_set p --model_name alexnet --device iphone --environment outdoor  --clip_target True --normalize_target True
python3 train_bigset.py --image_set p --model_name alexnet --device samsung --environment outdoor --clip_target True --normalize_target True --epochs 50 --lr 0.001
python3 linearplot.py   --image_set p --model_name alexnet --device samsung --environment outdoor --clip_target True --normalize_target True
python3 train_bigset.py --image_set p --model_name alexnet --device redmi --environment outdoor   --clip_target True --normalize_target True --epochs 50 --lr 0.001
python3 linearplot.py   --image_set p --model_name alexnet --device redmi --environment outdoor   --clip_target True --normalize_target True

# python3 train_bigset.py --image_set k --model_name alexnet --device iphone --environment all  --clip_target True --normalize_target True --epochs 50 --lr 0.001
# python3 linearplot.py   --image_set k --model_name alexnet --device iphone --environment all  --clip_target True --normalize_target True
# python3 train_bigset.py --image_set k --model_name alexnet --device samsung --environment all --clip_target True --normalize_target True --epochs 50 --lr 0.001
# python3 linearplot.py   --image_set k --model_name alexnet --device samsung --environment all --clip_target True --normalize_target True
# python3 train_bigset.py --image_set k --model_name alexnet --device redmi --environment all   --clip_target True --normalize_target True --epochs 50 --lr 0.001
# python3 linearplot.py   --image_set k --model_name alexnet --device redmi --environment all   --clip_target True --normalize_target True
# python3 train_bigset.py --image_set k --model_name alexnet --device iphone --environment indoor  --clip_target True --normalize_target True --epochs 50 --lr 0.001
# python3 linearplot.py   --image_set k --model_name alexnet --device iphone --environment indoor  --clip_target True --normalize_target True
# python3 train_bigset.py --image_set k --model_name alexnet --device samsung --environment indoor --clip_target True --normalize_target True --epochs 50 --lr 0.001
# python3 linearplot.py   --image_set k --model_name alexnet --device samsung --environment indoor --clip_target True --normalize_target True
# python3 train_bigset.py --image_set k --model_name alexnet --device redmi --environment indoor   --clip_target True --normalize_target True --epochs 50 --lr 0.001
# python3 linearplot.py   --image_set k --model_name alexnet --device redmi --environment indoor   --clip_target True --normalize_target True
# python3 train_bigset.py --image_set k --model_name alexnet --device iphone --environment outdoor  --clip_target True --normalize_target True --epochs 50 --lr 0.001
# python3 linearplot.py   --image_set k --model_name alexnet --device iphone --environment outdoor  --clip_target True --normalize_target True
# python3 train_bigset.py --image_set k --model_name alexnet --device samsung --environment outdoor --clip_target True --normalize_target True --epochs 50 --lr 0.001
# python3 linearplot.py   --image_set k --model_name alexnet --device samsung --environment outdoor --clip_target True --normalize_target True
# python3 train_bigset.py --image_set k --model_name alexnet --device redmi --environment outdoor   --clip_target True --normalize_target True --epochs 50 --lr 0.001
# python3 linearplot.py   --image_set k --model_name alexnet --device redmi --environment outdoor   --clip_target True --normalize_target True