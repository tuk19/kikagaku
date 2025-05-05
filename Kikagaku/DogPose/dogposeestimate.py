import io 
import base64
import cv2
import matplotlib.pyplot as plt
import os
from ultralytics import YOLO

def dog_image_estimate(image_path):
    # モデルと画像をロード
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(BASE_DIR, 'dog_100epochs_best.pt')
    model = YOLO(MODEL_PATH)
    results = model(image_path)

    # 骨格構造（例）
    '''
        0, 1, 2: 左前足
        3, 4, 5: 左後足
        6, 7, 8: 右前足
        9, 10, 11: 右後足
        14: 左耳付け根
        15: 右耳付け根
        16: 鼻
        17: 口
        18: 左耳
        19: 右耳
    '''
    skeleton = [
        (0, 1), (1, 2),
        (3, 4), (4, 5),
        (6, 7), (7, 8),
        (9, 10), (10, 11),
        (14, 15), (14, 18), (15, 19), 
    ]

    # 描画ベース画像（自動描画済み画像）
    img = results[0].plot()

    # キーポイント・バウンディングボックスを取得
    keypoints = results[0].keypoints.xy[0].cpu().numpy()   # shape: [num_kpts, 2]
    boxes = results[0].boxes.xyxy[0].cpu().numpy()         # shape: [4] (x1, y1, x2, y2)

    # OpenCV → RGBに変換して描画
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img_rgb)

    # 各キーポイントに番号と点を表示
    for i, (x, y) in enumerate(keypoints):
        if x > 0 and y > 0:
            plt.plot(x, y, 'ro', markersize=8)  # 点を大きく
            plt.text(x + 5, y - 5, str(i), color='yellow', fontsize=10, weight='bold')  # 番号

    # 骨格の線を描画
    for p1, p2 in skeleton:
        x1, y1 = keypoints[p1]
        x2, y2 = keypoints[p2]
        if x1 > 0 and y1 > 0 and x2 > 0 and y2 > 0:
            plt.plot([x1, x2], [y1, y2], 'g-', linewidth=2)  # 線

    plt.axis('off')

    buffer = io.BytesIO()
    plt.savefig(buffer, format="jpg", bbox_inches='tight')
    buffer.seek(0)
    image_jpg = buffer.getvalue()
    buffer.close()
    plt.close()

    base64_img = base64.b64encode(image_jpg).decode('utf-8')
    return base64_img