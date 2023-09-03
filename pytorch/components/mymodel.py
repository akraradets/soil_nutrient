import torchvision.models as models
import torch
from enum import Enum

class Models(Enum):
    mobilenet = 'mobilenet_v3_large'
    alexnet = 'alexnet'
    resnet = 'resnet50'
    efficientnet = 'efficientnet_v2_l'

def load_model(model_name:Models) -> torch.nn.Module:
    if(model_name == Models.mobilenet):
        return models.mobilenet_v3_large(num_classes=1)
    # elif(model_name == 'resnext101_64x4d'):
    #     model = models.resnext101_64x4d()
    #     model.fc = torch.nn.Linear(in_features=2048, out_features=1, bias=True)
    #     return model
    elif(model_name == Models.alexnet):
        model = models.alexnet()
        model.classifier[6] = torch.nn.Linear(in_features=4096, out_features=1, bias=True)
        return model
    elif(model_name == Models.resnet):
        model = models.resnet50()
        model.fc = torch.nn.Linear(in_features=2048, out_features=1, bias=True)
        return model
    elif(model_name == Models.efficientnet):
        model = models.efficientnet_v2_l()
        model.classifier.append(torch.nn.Linear(in_features=1000, out_features=1, bias=True))
        return model
    else:
        raise ValueError(f'Model name = {model_name} is not implemented!!')
    
def get_model(model_name:Models, image_set:str) -> torch.nn.Module:
    model = load_model(model_name=model_name)
    checkpoint = torch.load(f'./weight/{model_name}/{image_set}.pth')
    model.load_state_dict(checkpoint)
    return model