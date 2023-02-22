import torchvision.models as models
import torch

def load_model(model_name) -> torch.nn.Module:
    if(model_name == 'mobilenet_v3_large'):
        return models.mobilenet_v3_large(num_classes=1)
    # elif(model_name == 'resnext101_64x4d'):
    #     model = models.resnext101_64x4d()
    #     model.fc = torch.nn.Linear(in_features=2048, out_features=1, bias=True)
    #     return model
    elif(model_name == 'alexnet'):
        model = models.alexnet()
        model.classifier[6] = torch.nn.Linear(in_features=4096, out_features=1, bias=True)
        return model
    elif(model_name == 'resnet50'):
        model = models.resnet50()
        model.fc = torch.nn.Linear(in_features=2048, out_features=1, bias=True)
        return model
    elif(model_name == 'efficientnet_v2_l'):
        model = models.efficientnet_v2_l()
        model.classifier.append(torch.nn.Linear(in_features=1000, out_features=1, bias=True))
        return model
    else:
        raise ValueError(f'Model name = {model_name} is not implemented!!')
    
def get_model(model_name:str, image_set:str) -> torch.nn.Module:
    model = load_model(model_name=model_name)
    checkpoint = torch.load(f'./weight/{model_name}/{image_set}.pth')
    model.load_state_dict(checkpoint)
    return model