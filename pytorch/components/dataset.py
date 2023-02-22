import torch
from torch.utils.data import Dataset
from glob import glob
import os
import pandas as pd
from torchvision import io

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