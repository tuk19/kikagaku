from django.shortcuts import render
import numpy as np
from .forms import ImageUploadForm, PDFUploadForm
from .myocr import analyze_picture_bycv2, analyze_picture_bypillow
from .processpdf import discern_pdf, pdfocr

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
            
            # file_bytes = np.asarray(bytearray(image.read()), dtype=np.uint8)
            # image, result_list = analyze_picture_bycv2(file_bytes)
            uploaded = form.save()

            image, result_list = analyze_picture_bypillow(uploaded.image.file)
            joined_results = "\n".join(result_list)
            # print(joined_results)

            context = {
                'form': form,
                'image_type': image_type,
                'image': image,
                'result_text': joined_results,
            }
            uploaded.delete()
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


def pdf(request):
    if request.method == "POST":
        context = {}
        form = PDFUploadForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            pdf = request.FILES['pdf']
            uploaded = form.save()
            # discern = discern_pdf(uploaded.pdf.file)
            pdfocr(uploaded.pdf.path, 2)
            context = {
                'form': form,
                # 'error_message': discern
            }
            uploaded.delete()
            return render(request, 'imagetranscription/pdf.html', context)
        else:
            context = {
                'form': form,
            }
            return render(request, 'imagetranscription/pdf.html', context)
    else:
        form = PDFUploadForm()
        context = {
            'form': form,
        }
        return render(request, 'imagetranscription/pdf.html', context)