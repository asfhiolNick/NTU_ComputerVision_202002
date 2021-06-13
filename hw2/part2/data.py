import torch
import torchvision.transforms as transforms
from torchvision.datasets import ImageFolder
from PIL import Image
import glob, os
from torch.utils.data import Dataset, DataLoader

def get_dataloader(folder,batch_size=32):
    # Data preprocessing
    trans = transforms.Compose([transforms.Grayscale(), transforms.ToTensor(), transforms.Normalize((0.5,), (1.0,))])
    train_path, test_path = os.path.join(folder,'train'), os.path.join(folder,'valid')
    # Get dataset using pytorch functions
    train_set = ImageFolder(train_path, transform=trans)
    test_set =  ImageFolder(test_path,  transform=trans)
    train_loader = torch.utils.data.DataLoader(dataset=train_set, batch_size=batch_size, shuffle=True)
    test_loader  = torch.utils.data.DataLoader(dataset=test_set,  batch_size=batch_size, shuffle=False)
    print ('==>>> total trainning batch number: {}'.format(len(train_loader)))
    print ('==>>> total testing batch number: {}'.format(len(test_loader)))
    return train_loader, test_loader

class TestDataset(Dataset):
    """Test dataset."""
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.images = glob.glob(root_dir+'*.png')
        self.images.sort()
    def __len__(self):
        return len(self.images)
    def __getitem__(self, idx):
        img_name = self.images[idx]
        image = Image.open(img_name).convert('RGB')
        if self.transform:
            image = self.transform(image)
        return image, img_name.split('/')[-1]
