from django.shortcuts import render
from .forms import ImageUploadForm

# Create your views here.

def index(request):
    return render(request, ('imagetranscription/index.html'))

def image(request):
    if request.method == "POST":
        context = {}
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = request.FILES['image']
            image_type = image.content_type
            if image_type not in ['image/jpeg', 'image/png']:
                form = ImageUploadForm()
                context = {
                    'form': form,
                    'error_message': 'この画像はアップロードできません。JPEG または PNG 形式の画像のみアップロード可能です',
                }
                return render(request, 'imagetranscription/image.html', context)
            
            context = {
                'form': form,
                'image_type': image_type,
                'image': image,
            }
            return render(request, 'imagetranscription/image.html', context)
        else:
            form = ImageUploadForm()
            context = {
                'form': form,
                'error_message': 'このファイルはアップロードできません。JPET または PNG 形式の画像のみアップロード可能です',
            }
    else:
        form = ImageUploadForm()
        context = {
            'form': form,
        }
    return render(request, 'imagetranscription/image.html', context)