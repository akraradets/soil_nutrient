import mlflow
import torch
from torch.utils.data import DataLoader, random_split
import numpy as np
import matplotlib.pyplot as plt
import os
from copy import copy 
from typing import Tuple

from components.mymodel import Models
from components.helper import train_test
from components.dataset import *
from components.logger import *

import argparse

parser = argparse.ArgumentParser(description="An argument for the training data.")
parser.add_argument("--clip_target",type=bool, required=True)
parser.add_argument("--normalize_target",type=bool, required=True)
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
logger.info(args)

clip_target = args.clip_target
normalize_target = args.normalize_target
WORKERS = int(os.environ['WORKERS'])
image_set_dict = {
    'om': Imageset.om, 
    'p': Imageset.p, 
    'k': Imageset.k
    }
model_name_dict = {
    'alexnet': Models.alexnet,
    'resnet': Models.resnet,
    'mobilenet': Models.mobilenet
    }
device_dict = {
    'all': Devices.all,
    'iphone': Devices.iphone,
    'oppo': Devices.oppo,
    'samsung': Devices.samsung,
    'redmi': Devices.redmi,
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

batch_size = 0
if(model_name == Models.alexnet):
    batch_size = 200
elif(model_name == Models.mobilenet):
    batch_size = 75
elif(model_name == Models.resnet):
    batch_size = 30

def load_model(model_name:Models, image_set:Imageset, environment:Environments, device:Devices) -> Tuple[torch.nn.Module, pd.DataFrame]:
    search_name = f"{model_name.value}-{environment.value}-{device.value}"
    run_info = mlflow.search_runs(experiment_names=['Soil'],
                            filter_string=f"tags.mlflow.runName = '{search_name}'",)
    run_info = run_info.loc[run_info['params.Imageset'] == f'{image_set.value}']
    artifact_uri = run_info['artifact_uri'].iloc[0]
    loaded_model = mlflow.pytorch.load_model(f'{artifact_uri}/model')
    return loaded_model, run_info

model, run_info = load_model(model_name=model_name, image_set=image_set, environment=environment, device=device)
run_id = run_info.iloc[0].loc['run_id']
with mlflow.start_run(run_id=run_id):
    dataset = SoilDataset_bigset(imageset=image_set, 
                                device=device, 
                                environment=environment, 
                                preprocessing=Preprocessing.inferencing,
                                clip_target=clip_target,
                                normalize_target=normalize_target)
    loader  = DataLoader(dataset=dataset,  batch_size=batch_size, shuffle=False, num_workers=WORKERS)

    DEVICE = torch.device("cuda:0" if (torch.cuda.is_available()) else "cpu")
    logger.info(f"{DEVICE=}")
    model.eval()
    model.to(DEVICE)
    ys = []
    yhats = []
    pic_names = []
    with torch.no_grad():
        for X,y,pic_name in loader:
            X = X.to(DEVICE)
            yhat = model(X) #1. model
            yhat = yhat.detach().cpu().numpy()
            y = y.detach().cpu().numpy()

            pic_names.append(list(pic_name))
            ys.append(y.reshape(-1))
            yhats.append(yhat.reshape(-1))

    df = pd.DataFrame([np.hstack(ys) * dataset.max_value, np.hstack(yhats) * dataset.max_value, np.hstack(pic_names)]).T
    df.rename(columns = {
        0:'Target',
        1:'Predict',
        2:'Image name'
    }, inplace=True)
    df.set_index('Image name', inplace=True)
    artifact_name:str = os.path.join('artifact','inference.csv')
    df.to_csv(artifact_name)
    mlflow.log_artifact(artifact_name)
    df = df.sort_values(by=['Target'])
    fig, ax = plt.subplots(figsize=(10,5))
    ax.scatter(range(len(df)), df['Predict'], marker='.', alpha=0.7, label='Predict')
    ax.scatter(range(len(df)), df['Target'], marker='.', alpha=0.4, label='Actual')
    ax.grid()
    ax.legend()
    ax.set_xticklabels([])
    ax.set_title(f"{model_name.value} image={image_set.value}")
    mlflow.log_figure(fig, 'inference.png')