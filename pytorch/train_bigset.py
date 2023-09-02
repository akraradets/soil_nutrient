import mlflow
import torch
from torch.utils.data import DataLoader, random_split

import os
from copy import copy 

from components.mymodel import load_model, Models
from components.helper import train_test
from components.dataset import *
from components.logger import *

import argparse

parser = argparse.ArgumentParser(description="List fish in aquarium.")
parser.add_argument("--clip_target",type=bool, required=True)
parser.add_argument("--normalize_target",type=bool, required=True)
parser.add_argument("--epochs",type=int, required=True)
parser.add_argument("--lr",type=float, required=True)
parser.add_argument("--image_set",type=str, required=True)
parser.add_argument("--model_name",type=str, required=True)
parser.add_argument("--device",type=str, required=True)
parser.add_argument("--environment",type=str, required=True)
args = parser.parse_args()



mlflow.set_tracking_uri("https://web-mlflow.akraradets.duckdns.org")
mlflow.set_experiment(experiment_name='Soil')

# Logger
init_logger(name='main', filename='train_bigset')
logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)

clip_target = args.clip_target
normalize_target = args.normalize_target
epochs = args.epochs
lr = args.lr
WORKERS = int(os.environ['WORKERS'])
image_set_dict = {
    'om': Imageset.om, 
    'p': Imageset.p, 
    'k': Imageset.k
    }
model_name_dict = {
    'alexnet': Models.alexnet,
    'restnet': Models.restnet,
    'mobilenet': Models.mobilenet
    }
device_dict = {
    'all': Devices.all,
    'iphone': Devices.iphone,
    'oppo': Devices.oppo,
    'samsung': Devices.samsung,
    'iphone': Devices.iphone,
}
environment_dict = {
    'all': Environments.all,
    'indoor': Environments.indoor,
    'outdoor': Environments.outdoor,

}

image_set = image_set_dict[args.image_set]
model_name = model_name_dict[args.model_name]
device = device_dict[args.device]
environment = environment_dict[args.environment]

with mlflow.start_run(run_name=f"{image_set.value}") as parent_run:
    with mlflow.start_run(run_name=f"{model_name.value}", nested=True) as child_run:
        batch_size = 0
        if(model_name == Models.alexnet):
            batch_size = 200
        elif(model_name == Models.mobilenet):
            batch_size = 100
        elif(model_name == Models.restnet):
            batch_size = 50

        params:dict = dict({
            'epochs': epochs,
            'lr': lr,
            'batch_size': batch_size,
            'Imageset': image_set.value,
            'Device': device.value,
            'Environment': environment.value,
            'model_name': model_name.value,
            'clip_target': clip_target,
            'normalize_target': normalize_target
        })

        DEVICE = torch.device("cuda:0" if (torch.cuda.is_available()) else "cpu")
        logger.info(f"{DEVICE=}")
        full_train_dataset = SoilDataset_bigset(imageset=image_set, 
                                    device=device, 
                                    environment=environment, 
                                    preprocessing=Preprocessing.training,
                                    clip_target=clip_target,
                                    normalize_target=normalize_target)
        train_dataset, test_dataset = random_split(dataset=full_train_dataset, lengths=[0.8,0.2], generator=torch.Generator().manual_seed(42))
        train_dataset.dataset.preprocessing = Preprocessing.training.value # type:ignore
        test_dataset.dataset.preprocessing  = Preprocessing.inferencing.value # type:ignore

        logger.info(f"{len(full_train_dataset)} {len(train_dataset)=} {len(test_dataset)=}")
        mlflow.log_param("train_size",len(train_dataset))
        mlflow.log_param("test_size",len(test_dataset))
        mlflow.log_params(params)
        # train model
        model = load_model(model_name=model_name)
        train_loader = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True,  num_workers=WORKERS)
        test_loader  = DataLoader(dataset=test_dataset,  batch_size=batch_size, shuffle=False, num_workers=WORKERS)
        train_test(model=model, train_loader=train_loader, test_loader=test_loader, epochs=epochs, lr=lr, DEVICE=DEVICE)