import io 
import base64
import cv2
import matplotlib.pyplot as plt
from ultralytics import YOLO

import subprocess
import os

def convert_to_h264(input_path, output_path):
    subprocess.run([
        'ffmpeg', '-y', '-i', input_path,
        '-vcodec', 'libx264', '-acodec', 'aac', output_path
    ])


def estimate_video_pose(input_path, output_path, fps_rate):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(BASE_DIR, 'yolov8n-pose.pt')
    model = YOLO(MODEL_PATH)
    cap = cv2.VideoCapture(input_path)
    fps = cap.get(cv2.CAP_PROP_FPS) * fps_rate
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        annotated_frame = results[0].plot()
        out.write(annotated_frame)

    cap.release()
    out.release()

def estimate_image_pose(input_path):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(BASE_DIR, 'yolov8n-pose.pt')
    model = YOLO(MODEL_PATH)
    results = model(input_path)
    img = results[0].plot()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img_rgb)

    plt.axis('off')

    buffer = io.BytesIO()
    plt.savefig(buffer, format="jpg", bbox_inches='tight')
    buffer.seek(0)
    image_jpg = buffer.getvalue()
    buffer.close()
    plt.close()

    base64_img = base64.b64encode(image_jpg).decode('utf-8')
    return base64_img