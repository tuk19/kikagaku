from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from .forms import ImageUploadform
from .predict import predict_image_top2_with_gradcam_224, predict_image_top2_with_gradcam
from io import BytesIO
import copy

def index(request):
    if request.method == "POST":
        context = {}
        form = ImageUploadform(request.POST, request.FILES)
        if form.is_valid():
            image = request.FILES['image']
            # 画像の MIME タイプを取得
            image_type = image.content_type
            if image_type not in ['image/jpeg', 'image/png']:
                form = ImageUploadform()
                context = {
                    'form': form,
                    'error_message': 'この画像はアップロードできません。JPEG または PNG 形式の画像のみアップロード可能です',
                }

                return render(request, 'imageclassification/index.html', context)

            image_copy = BytesIO(image.read())
            image_copy.seek(0)
            image_for_display = copy.deepcopy(image_copy)
            image_for_predict = copy.deepcopy(image_copy)
            
            # 224 x 224 のGrad-CAMを表示
            result1, result2, gradcam1_b64, gradcam2_b64 = predict_image_top2_with_gradcam_224(image_for_predict)

            # 元画像サイズと同じサイズのGrad-CAMを表示
            # result1, result2, gradcam_b64= predict_image_top2_with_gradcam(image_for_predict)

            image_for_display.seek(0)
            image.file = image_for_display

            context = {
                'form': form,
                'image_type': image_type,
                'image': image,
                'result1': result1,
                'result2': result2,
                'gradcam1': gradcam1_b64,
                'gradcam2': gradcam2_b64
            }

            return render(request, 'imageclassification/index.html', context)
        else:
            form = ImageUploadform()
            context = {
                'form': form,
                'error_message': 'このファイルはアップロードできません。JPEG または PNG 形式の画像のみアップロード可能です',
            }
    else:
        form = ImageUploadform()
        context = {
            'form': form,
        }

    return render(request, 'imageclassification/index.html', context)
