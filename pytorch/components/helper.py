import torch
from torch.utils.data import DataLoader
def train(model:torch.nn.Module, loader:DataLoader, epochs:int, lr:float, DEVICE:str):
    J_fn = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    model.to(DEVICE)

    import time
    train_losses = []
    #for epochs
    for e in range(epochs):
        #for train loader
        total_corr = 0
        for b, (image, label, _) in enumerate(loader):
            
            start_time = time.time()
            
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
            #total time
            total_time = time.time() - start_time
            
            # if (b+1) % 20 == 0:
            #     print(b, train_loss)
            # print(f"Epoch: {e} - Batch: {b} - Train Loss: {train_loss:.2f} - Total Time: {total_time:.2f}s")
        if((e+1)%10 == 0):
            print(e)
    return model, train_losses