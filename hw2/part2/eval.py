import os, sys
import csv
import numpy as np
import torch
import torch.nn as nn
from torch.autograd import Variable
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
from model import ConvNet, MyNet
from data import TestDataset


if __name__ == "__main__":
    data_path, model_type, output = sys.argv[1], sys.argv[2], sys.argv[3]

    if model_type == 'conv':
        model = ConvNet()
        model.load_state_dict(torch.load('checkpoint/ConvNet.pth'))
    elif model_type == 'mynet':
        model = MyNet()
        model.load_state_dict(torch.load('checkpoint/MyNet.pth'))
    #print(model)
    #######################################################################
    # Modifiy this part to load your trained model
    # TODO
    #######################################################################


    use_cuda = torch.cuda.is_available()
    if use_cuda:
        model.cuda()
    model.eval()

    # Load data
    trans = transforms.Compose([transforms.Grayscale(),transforms.ToTensor(), transforms.Normalize((0.5,), (1.0,))])
    test_set = TestDataset(data_path, transform=trans)
    print('Length of Testing Set:', len(test_set))
    test_loader = DataLoader(dataset=test_set, batch_size=1, shuffle=False)

    # testing
    prediction = []
    with torch.no_grad():
        for batch_idx, (x,name) in enumerate(test_loader):
            if use_cuda:
                x = x.cuda()
            out = model(x)
            _, pred_label = torch.max(out, 1)
            prediction.append((name[0][:-4], pred_label.item()))

    with open(output, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['id','label'])
        for i in prediction:
            writer.writerow([i[0], i[1]])

