import torch
import torch.nn as nn
import torch.nn.functional as F

class ConvNet(nn.Module):
    def __init__(self):
        super(ConvNet, self).__init__()
        # TODO
        self.cnn = nn.Sequential(                                   #1@ 28*28 (Input Dim)
            nn.Conv2d(1, 6, kernel_size=(5,5), stride=(1,1)),       #6@ 24*24
            nn.ReLU(inplace=True),
            nn.AvgPool2d(2, 2, 0),                                  #6@ 12*12
            nn.Conv2d(6, 16, kernel_size=(5,5), stride=(1,1)),      #16@ 8*8
            nn.ReLU(inplace=True),
            nn.AvgPool2d(2, 2, 0),                                  #16@ 4*4
        )

        self.fc = nn.Sequential(
            nn.Linear(in_features=256, out_features=120, bias=True),
            nn.ReLU(inplace=True),
            nn.Linear(in_features=120, out_features=84, bias=True),
            nn.ReLU(inplace=True),
            nn.Linear(in_features=84, out_features=10, bias=True),
        )


    def forward(self, x):
        # TODO
        out = self.cnn(x)
        out = out.view(out.size()[0], -1)      
        out = self.fc(out)
        return out

    def name(self):
        return "ConvNet"

class MyNet(nn.Module):
    def __init__(self):
        super(MyNet, self).__init__()
        # TODO
        self.cnn = nn.Sequential(                                   #1@ 28*28 (Input Dim)
            nn.Conv2d(1, 6, kernel_size=(5,5), stride=(1,1)),       #6@ 24*24
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2, 0),                                  #6@ 12*12
            nn.Conv2d(6, 16, kernel_size=(5,5), stride=(1,1)),      #16@ 8*8
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2, 0),                                  #16@ 4*4
            nn.Conv2d(16, 40, kernel_size=(3,3), stride=(1,1)),     #40@ 2*2
            nn.ReLU(inplace=True),
        )

        self.fc = nn.Sequential(
            nn.Dropout(),
            nn.Linear(in_features=160, out_features=120, bias=True),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(in_features=120, out_features=84, bias=True),
            nn.ReLU(inplace=True),
            nn.Linear(in_features=84, out_features=10, bias=True),
        )

    def forward(self, x):
        # TODO
        out = self.cnn(x)
        out = out.view(out.size()[0], -1)      
        out = self.fc(out)
        return out

    def name(self):
        return "MyNet"

