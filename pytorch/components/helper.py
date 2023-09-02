import mlflow
from mlflow.models.signature import infer_signature
from mlflow.pytorch import log_model
import torch
from torch.utils.data import DataLoader
import os
import asyncio
import math
def train(model:torch.nn.Module, loader:DataLoader, epochs:int, lr:float, DEVICE:str):
    J_fn = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    model.to(DEVICE)

    import time
    train_losses = []
    #for epochs
    best_loss = math.inf

    for e in range(epochs):
        #for train loader
        total_corr = 0
        epoch_loss = 0
        start_time = time.time()
        for b, (image, label, _) in enumerate(loader):
            # print(f'start:{b}')
            #image: (B, C, W, H)
            #label: (B)
            image = image.to(DEVICE)
            label = label.to(DEVICE)
            
            yhat = model(image) #1. model
            train_loss = J_fn(yhat.reshape(-1), label.reshape(-1)) #2. loss
            #2.1 collect the loss and acc

            optimizer.zero_grad() #3. zero_grad
            train_loss.backward() #4. backward
            optimizer.step() #5. step
            
            train_losses.append(train_loss.detach().cpu())
            epoch_loss += train_loss.detach().cpu()
            # print(f'stop:{b}')
            #total time
            
            # if (b+1) % 20 == 0:
            #     print(b, train_loss)
            # print(f"Epoch: {e} - Batch: {b} - Train Loss: {train_loss:.2f} - Total Time: {total_time:.2f}s")
        # if((e+1)%10 == 0):
        #     print(e)
        total_time = time.time() - start_time
        print(total_time, e, epoch_loss)
        # Check if model improve?
        mlflow.log_metric('epoch_loss', epoch_loss, step=e)
        if( epoch_loss <= best_loss ):
            print('save model!!')
            log_model(pytorch_model=model,artifact_path="model")
            best_loss = epoch_loss
                
    return model, train_losses

def train_test(model:torch.nn.Module, train_loader:DataLoader, test_loader:DataLoader, epochs:int, lr:float, DEVICE:torch.device):
    J_fn = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    model.to(DEVICE)

    import time
    #for epochs
    best_loss = math.inf

    for e in range(epochs):
        start_time = time.time()
        model.train()
        train_mse = 0
        for b, (image, label, _) in enumerate(train_loader):
            # print(f'start:{b}')
            #image: (B, C, W, H)
            #label: (B)
            image = image.to(DEVICE)
            label = label.to(DEVICE)
            
            yhat = model(image) #1. model
            train_loss = J_fn(yhat.reshape(-1), label.reshape(-1)) #2. loss
            #2.1 collect the loss and acc

            optimizer.zero_grad() #3. zero_grad
            train_loss.backward() #4. backward
            optimizer.step() #5. step
            
            train_mse += train_loss.detach().cpu()

        total_time = time.time() - start_time
        print(total_time, e, train_mse)
        mlflow.log_metric('train_mse', train_mse, step=e)
        if( train_mse <= best_loss ):
            print('save model!!')
            log_model(pytorch_model=model,artifact_path="model")
            best_loss = train_mse
        # Testing
        model.eval()
        test_mse = 0
        for b, (image, label, _) in enumerate(test_loader):
            image = image.to(DEVICE)
            label = label.to(DEVICE)
            yhat = model(image) #1. model
            test_loss = J_fn(yhat.reshape(-1), label.reshape(-1)) #2. loss
            test_mse += test_loss.detach().cpu()
        mlflow.log_metric('test_mse', test_mse, step=e)
                
    return model