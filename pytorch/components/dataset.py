import torch
from torch.utils.data import Dataset
from glob import glob
import os
import pandas as pd
from torchvision import io
from enum import Enum

class SoilDataset(Dataset):
    def __init__(self, dataset_path:str, image_set:str, transform=None):
        assert os.path.exists(dataset_path), f"Path is not exist."
        # dataset_path = './dataset/testkit_1/'
        label_file = os.path.join(dataset_path,'meta.csv')
        assert os.path.exists(label_file), f"File label 'meta.csv' is not exist in {dataset_path}."
        self.labels = pd.read_csv(label_file)

        image_folder = os.path.join(dataset_path, image_set)
        assert os.path.exists(image_folder), f"image_set={image_set} is not exists in {dataset_path}."
        self.imgs = glob(os.path.join(image_folder,'*'))
        print(f"Found {len(self.imgs)} images in {image_folder}.")
        
        self.transform = transform

    def __len__(self):
        return len(self.imgs)

    def __getitem__(self, idx):
        # './dataset/testkit_1/insideroom_1/1 (1).jpg'
        img_path = self.imgs[idx]
        # './dataset/testkit_1/insideroom_1, 1 (1).jpg'
        _, img_name_w_ext = os.path.split(img_path)
        # 1 (1)
        img_name = os.path.splitext(img_name_w_ext)[0]
        # 1
        img_id = img_name.split(' ')[0]
        y = self.labels.values[self.labels.id == int(img_id)][0][1]
        y = torch.tensor(y)
        # print(y)
        X = io.read_image(img_path)
        if self.transform:
            X = self.transform(X)
        return X.float(), y.float(), img_name_w_ext
    
class SoilDataset_phone(Dataset):
    def __init__(self, dataset_path:str, image_set:str, transform=None):
        assert os.path.exists(dataset_path), f"Path is not exist."

        image_folder = os.path.join(dataset_path, image_set)
        assert os.path.exists(image_folder), f"image_set={image_set} is not exists in {dataset_path}."
        self.imgs = glob(os.path.join(image_folder,'*'))
        print(f"Found {len(self.imgs)} images in {image_folder}.")
        
        self.transform = transform

    def __len__(self):
        return len(self.imgs)

    def __getitem__(self, idx):
        img_path = self.imgs[idx]
        path, img_name_w_ext = os.path.split(img_path)
        name, ext = os.path.splitext(img_name_w_ext)
        # print(name)
        id, phone_brand, OM, lab_no, soil_character, place, variant = name.split('_')
        y = float(OM)
        y = torch.tensor(y)
        # print(y)
        X = io.read_image(img_path)
        if self.transform:
            X = self.transform(X)
        return X.float(), y.float(), img_name_w_ext
    
class Devices(Enum):
    iphone = 'Iphone'
    oppo = 'Oppo'
    redmi = 'Redmi'
    samsung = 'Samsung'
    all = '*'

class Environments(Enum):
    indoor = 'Indoor'
    outdoor = 'Outdoor'
    all = '*'

class Imageset(Enum):
    om = 'OM'
    p = 'P'

class SoilDataset_bigset(Dataset):
    def __init__(self, imageset:Imageset, device:Devices, environment:Environments, transform=None):
        # BasePath of the dataset
        dataset_path:str = './dataset/bigset/'
        assert os.path.exists(dataset_path), f"{dataset_path=} is not exist."
        # Inside this path there must be a list of folders arange by mobile phone. Use device enum.
        # Inside those mobile phone are 2 folders indicate the environment the image was taken in. Use environment enum.
        image_folder = os.path.join(dataset_path, imageset.value, device.value, environment.value)
        self.imgs = glob(os.path.join(image_folder,'*/*'))
        print(f"Found {len(self.imgs)} images in {image_folder}.")

        # Load csv file for lookup the target value
        target_path:str = os.path.join(dataset_path,imageset.value,'meta.csv')
        self.target_df = pd.read_csv(target_path, index_col='id')

        self.signature = os.path.join(imageset.value,device.value,environment.value)
        self.transform = transform

    def get_target(self, img_path:str) -> float:
        assert len(img_path.split('/')) == 8, f"Expect img_path to have 8 folders but got {img_path=}"
        target_id = int(img_path.split('/')[6])
        return self.target_df.loc[target_id] # type:ignore
        
    def __len__(self):
        return len(self.imgs)

    def __getitem__(self, idx):
        img_path = self.imgs[idx]
        y = self.get_target(img_path=img_path)
        y = torch.tensor(y)
        X = io.read_image(img_path)
        if self.transform:
            X = self.transform(X)
        return X.float(), y.float(), img_path