import torch
import torch.nn as nn
import torch.nn.functional as F
import torchaudio
from .resnet_model import AudioClassifier

from Kikagaku.settings import BASE_DIR
import os

mel_transform = torchaudio.transforms.MelSpectrogram(
    sample_rate=16000,
    n_mels=64
)

class_list = [
    'DragonQuest',
    'FinalFantasy',
]

ckpt_path = os.path.join(BASE_DIR, 'MusicClassification/best_musicmodel_RN18.ckpt')
model = AudioClassifier.load_from_checkpoint(ckpt_path)

def fix_length(waveform, sr, target_seconds=10):
    target_length = sr * target_seconds
    current_length = waveform.shape[1]
    if current_length < target_length:
        padding = target_length - current_length
        waveform = torch.nn.functional.pad(waveform, (0, padding))
    elif current_length > target_length:
        waveform = waveform[:, :target_length]
        # print('current_length > target_length')
    return waveform

def predict_music(file_path):
    model.eval()
    waveform, sr = torchaudio.load(file_path)

    # ステレオ → モノラル
    if waveform.shape[0] > 1:
        waveform = waveform.mean(dim=0, keepdim=True)
    
    # サンプリングレート統一
    if sr != 16000:
        resampler = torchaudio.transforms.Resample(sr, 16000)
        waveform = resampler(waveform)
        sr = 16000

    waveform = fix_length(waveform, sr)

    mel = mel_transform(waveform)  # [1, 64, time]
    # print(mel.shape)
    mel = mel.squeeze(0)           # [64, time]
    mel = mel.unsqueeze(0)         # [1, 64, time]
    mel = mel.repeat(3, 1, 1)      # [3, 64, time]
    mel = mel.unsqueeze(0)         # バッチ次元追加 → [1, 3, 64, time]

    with torch.no_grad():
        y = model(mel)             # [1, num_classes]

    probs = F.softmax(y, dim=1)
    pred, ind = torch.topk(probs, k=1, dim=1)
    print(f'pred: {pred}, ind: {ind}')
    pred = round(pred.item(), 3) * 100
    ind = ind.item()
    print(f'pred: {pred}, ind: {ind}')

    pred_class = class_list[ind] 

    return pred, pred_class