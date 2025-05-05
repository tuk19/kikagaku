from django.shortcuts import render
from django.conf import settings
from .forms import ImageUploadForm
from .dogposeestimate import dog_image_estimate
from io import BytesIO
import os
import copy

def index(request):
    if request.method == "POST":
        context = {}
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = request.FILES['image']
            # 画像の MIME タイプを取得
            image_type = image.content_type
            if image_type not in ['image/jpeg', 'image/png']:
                form = ImageUploadForm()
                context = {
                    'form': form,
                    'error_message': 'この画像はアップロードできません。JPEG または PNG 形式の画像のみアップロード可能です',
                }

                return render(request, 'dogpose/index.html', context)

            temp_path = os.path.join(settings.MEDIA_ROOT, 'temp_img.jpg')
            with open(temp_path, 'wb+') as f:
                for chunk in image.chunks():
                    f.write(chunk)

            base64_img = dog_image_estimate(temp_path)
            os.remove(temp_path)

            context = {
                'form': form,
                'error_message': None,
                'image_type': 'image/jpeg',
                'image': base64_img,
            }
            return render(request, 'dogpose/index.html', context)
        else:
            form = ImageUploadForm()
            context = {
                'form': form,
                'error_message': 'このファイルはアップロードできません。JPEG または PNG 形式の画像のみアップロード可能です',
            }
            return render(request, 'dogpose/index.html', context)
    else:
        form = ImageUploadForm()
        context = {
            'form': form,
        }

    return render(request, 'dogpose/index.html', context)