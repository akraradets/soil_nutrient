import mlflow
import mlflow.pytorch
import pickle
import torch
from torchvision import transforms
from PIL import Image

import sys
import os
import logging
# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__)) 
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
# adding the parent directory to 
# the sys.path.
sys.path.append(parent)

from app_config import *

logger = logging.getLogger('main')

def _save_cache(model, name:str):
    with open(name, 'wb') as handle:
        pickle.dump(model, handle, protocol=pickle.HIGHEST_PROTOCOL)

def _load_cache(name:str):
    with open(name, 'rb') as handle:
        model = pickle.load(handle)
    return model

def load_model_to_cache():
    if(os.path.exists(MODEL_PATH) == False):
        os.makedirs(MODEL_PATH)
    
    names = [MODEL_K,MODEL_P,MODEL_OM]
    for name in names:
        full_path = os.path.join(MODEL_PATH,name)
        if(os.path.exists(full_path) == False):
            logger.info(f"model={full_path} is not in cache.")
            model = mlflow.pytorch.load_model(model_uri=f"models:/{name}/{MODEL_STAGE}", map_location=torch.device('cpu'))
            _save_cache(model=model, name=full_path)
            logger.info(f"model={full_path} loadded in cache.")

def load_model(name:str) -> torch.nn.Module:
    full_path = os.path.join(MODEL_PATH,name)
    model = _load_cache(name=full_path)
    return model


def preprocess_image(image:Image) -> Image:
    process  = transforms.Compose([
        transforms.Resize(350),
        transforms.CenterCrop(224),
    ])
    processed_image = process(image)
    return processed_image

def to_tensor(image:Image) -> torch.tensor:
    process  = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
    ])
    processed_image = process(image)
    processed_image.unsqueeze_(0)
    return processed_image

def prediction(model:torch.nn.Module, image:Image) -> (Image,float):
    process_image:Image = preprocess_image(image)
    X:torch.tensor = to_tensor(process_image)

    y = model(X)[0][0]
    predict = float(y)

    return process_image, predict