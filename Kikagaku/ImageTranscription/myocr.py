import easyocr
import cv2
from PIL import Image, ImageDraw, ImageEnhance
import numpy as np
import io
import base64
import os
import uuid
import tempfile


reader = easyocr.Reader(['en', 'ja'], verbose=True)
# reader = easyocr.Reader(['en'], verbose=True)


def analyze_picture_bycv2(file_bytes, link_threshold=0.3, mag_ratio=1.2):
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    results = reader.readtext(img, link_threshold=link_threshold, mag_ratio=mag_ratio)
    print(results)
    result_list = []

    for result in results:
        points = [tuple(map(int, pt)) for pt in result[0]]
        for i in range(len(points)):
            cv2.line(img, points[i], points[(i+1)%4], (0, 0, 255), 3)
        result_list.append(result[1])
        # print(result[1])

    _, buffer = cv2.imencode('.jpg', img)
    img_str = base64.b64encode(buffer).decode('utf-8')

    return img_str, result_list


def analyze_picture_bypillow(image_file_path):
    print(f"print1: {image_file_path}")
    # image = Image.open(io.BytesIO(image.read()))
    image = Image.open(image_file_path)
    image = image.convert('RGB')
    image.thumbnail((800, 800))
    # image = ImageEnhance.Brightness(image).enhance(1.2)
    # image = ImageEnhance.Contrast(image).enhance(2)
    draw = ImageDraw.Draw(image)

    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, f"{uuid.uuid4()}.jpg")
    # image_np = np.array(image)
    image.save(temp_path, format="JPEG")
    print(f"print2: {temp_path}")
    results = reader.readtext(temp_path, link_threshold=0.3, mag_ratio=1.2, detail=1)
    # results = reader.readtext(temp_path)
    print(f"print3: {results}")
    result_list = []

    for result in results:
        p0, p1, p2, p3 = result[0]
        draw.line([*p0, *p1, *p2, *p3, *p0], fill='red', width=3)
        result_list.append(result[1])
        print(f"print4: {result[1]}")
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')

    os.remove(temp_path)

    return img_str, result_list