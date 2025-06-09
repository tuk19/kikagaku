import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.nn.functional as F
import pytorch_lightning as pl
from torchvision import transforms, models
from .resnet_model import ResNet18Classifier
from PIL import Image
import cv2

from Kikagaku.settings import BASE_DIR
import os
import base64



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

# Grad-CAM用のフック用変数
features = None
gradients = None

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


def save_features_hook(module, input, output):
    global features
    features = output.detach()

def save_gradient_hook(module, grad_input, grad_output):
    global gradients
    gradients = grad_output[0].detach()

def generate_gradcam_224(image_tensor, class_idx):
    # フックの登録（layer4の最後を使うのが一般的）
    target_layer = model.model.layer4[-1]
    target_layer.register_forward_hook(save_features_hook)
    target_layer.register_full_backward_hook(save_gradient_hook)

    model.zero_grad()
    output = model(image_tensor)
    class_score = output[0, class_idx]
    class_score.backward()

    # 平均勾配を計算
    weights = torch.mean(gradients, dim=(2, 3), keepdim=True)
    cam = torch.sum(weights * features, dim=1).squeeze().cpu().numpy()

    cam = np.maximum(cam, 0)
    cam = cv2.resize(cam, (224, 224))
    cam = cam - np.min(cam)
    cam = cam / np.max(cam)
    cam = np.uint8(255 * cam)
    heatmap = cv2.applyColorMap(cam, cv2.COLORMAP_JET)

    return heatmap

def predict_image_top2_with_gradcam_224(image):
    image = Image.open(image).convert('RGB')
    image_tensor = transform(image).unsqueeze(0)
    model.eval()

    with torch.no_grad():
        y = model(image_tensor)
        probs = F.softmax(y, dim=1)
        top2_probs, top2_indices = torch.topk(probs, k=2, dim=1)

    # Grad-CAM（上位1位のみ）
    image_tensor.requires_grad = True
    heatmap = generate_gradcam_224(image_tensor, top2_indices[0][0].item())

    # 元画像をcv2に変換
    original_image = np.array(image.resize((224, 224)))
    original_image = cv2.cvtColor(original_image, cv2.COLOR_RGB2BGR)
    overlay = cv2.addWeighted(original_image, 0.6, heatmap, 0.4, 0)

    # base64に変換
    _, buffer = cv2.imencode('.png', overlay)
    heatmap_b64 = base64.b64encode(buffer).decode()

    top2_classes = [class_list[i] for i in top2_indices[0]]
    return top2_classes[0], top2_classes[1], heatmap_b64

def generate_gradcam(image_tensor, class_idx):
    # Grad-CAM用のターゲット層（layer4 の最後）
    target_layer = model.model.layer4[-1]
    target_layer.register_forward_hook(save_features_hook)
    target_layer.register_full_backward_hook(save_gradient_hook)

    model.zero_grad()
    output = model(image_tensor)
    class_score = output[0, class_idx]
    class_score.backward()

    # 勾配の平均を取る（Global Average Pooling）
    weights = torch.mean(gradients, dim=(2, 3), keepdim=True)
    cam = torch.sum(weights * features, dim=1).squeeze().cpu().numpy()

    # ReLU適用
    cam = np.maximum(cam, 0)

    # 正規化（0〜1）
    cam = cam - np.min(cam)
    cam = cam / np.max(cam + 1e-8)  # divide by zero 防止

    # 0〜255 の画像に変換（ここでは resize しない！）
    cam = np.uint8(255 * cam)

    return cam  # ← ヒートマップ前の raw CAM を返す

def predict_image_top2_with_gradcam(image):
    image = Image.open(image).convert('RGB')
    image_tensor = transform(image).unsqueeze(0)
    model.eval()

    with torch.no_grad():
        y = model(image_tensor)
        probs = F.softmax(y, dim=1)
        top2_probs, top2_indices = torch.topk(probs, k=2, dim=1)

    # Grad-CAM（上位1位のみ）
    image_tensor.requires_grad = True
    cam_raw = generate_gradcam(image_tensor, top2_indices[0][0].item())

    # 元画像のサイズ取得（PIL→np→cv2形式）
    original_image = np.array(image)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_RGB2BGR)
    original_size = (original_image.shape[1], original_image.shape[0])  # (width, height)

    # CAMを元画像サイズに拡大
    cam_resized = cv2.resize(cam_raw, original_size)

    # カラーヒートマップに変換
    heatmap = cv2.applyColorMap(cam_resized, cv2.COLORMAP_JET)

    # オーバーレイ画像作成
    overlay = cv2.addWeighted(original_image, 0.6, heatmap, 0.4, 0)

    # base64エンコードしてHTMLで表示可能に
    _, buffer = cv2.imencode('.png', overlay)
    heatmap_b64 = base64.b64encode(buffer).decode()

    # クラス名変換
    top2_classes = [class_list[i] for i in top2_indices[0]]
    return top2_classes[0], top2_classes[1], heatmap_b64
