import torch
import torch.nn as nn
from torchvision import models

import pytorch_lightning as pl

class AudioClassifier(pl.LightningModule):
    def __init__(self, num_classes=2):
        super().__init__()
        self.model = models.resnet18(pretrained=True)
        in_features = self.model.fc.in_features
        self.model.fc = nn.Linear(in_features, num_classes)

    def forward(self, x):
        return self.model(x)