from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from .forms import ImageUploadform

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

            context = {
                'form': form,
                'image_type': image_type,
                'image': image
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
