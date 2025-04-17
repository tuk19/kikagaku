import torch
import torch.nn as nn
import torch.nn.functional as F
import pytorch_lightning as pl
from torchvision import transforms, models
from .resnet_model import ResNet18Classifier
from PIL import Image

from Kikagaku.settings import BASE_DIR
import os



transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

class_list = [
    'バツ丸',
    'シナモロール',
    'ハンギョドン',
    'けろけろけろっぴ',
    'ハローキティ',
    'クロミ',
    'マイメロディ',
    'ポチャッコ',
    'ポムポムプリン',
    'タキシードサム'
]

ckpt_path = os.path.join(BASE_DIR, 'ImageClassification/best_model_RN18.ckpt')
model = ResNet18Classifier.load_from_checkpoint(ckpt_path)

def predict_image(image):
    image = Image.open(image).convert('RGB')
    # バッチサイズ1に合わせてテンソルを変換
    image = transform(image).unsqueeze(0)
    
    model.eval()

    with torch.no_grad():
        y = model(image)

    y = torch.argmax(y, dim=1)
    # print(y)
    predict_class = class_list[y]

    return predict_class

def predict_image_top2(image):
    image = Image.open(image).convert('RGB')
    image = transform(image).unsqueeze(0)

    model.eval()

    with torch.no_grad():
        y = model(image)

    probs = F.softmax(y, dim=1)

    # 上位2つのインデックスを取得
    top2_probs, top2_indices = torch.topk(probs, k=2, dim=1)

    # インデックスからクラス名へ変換
    top2_classes = [class_list[i] for i in top2_indices[0]]
    # print(top2_classes)

    return top2_classes[0], top2_classes[1]