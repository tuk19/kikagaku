from django.shortcuts import render
from django.conf import settings
import numpy as np
from .forms import ImageUploadForm, PDFUploadForm
from .myocr import analyze_picture_bycv2, analyze_picture_bypillow
from .processpdf import discern_pdf, pdfocr, pdf_to_text
import os
import fitz

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
        error_message = None
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf = request.FILES['pdf']
            uploaded = form.save()
            discern = discern_pdf(uploaded.pdf.file)
            if discern == 'image':
                page_number = 2
                pdfocr(uploaded.pdf.path, page_number)
                context = {
                    'form': form,
                }
                uploaded.delete()
                return render(request, 'imagetranscription/pdf.html', context)
            else:
                page_number = request.POST['page_number']
                doc = fitz.open(uploaded.pdf.file)
                total_pages = doc.page_count
                try:
                    int(page_number)
                    if int(page_number) < 1 or int(page_number) > total_pages:
                        error_message = f'指定するページ番号は 1 〜 {total_pages} の範囲で設定してください。'
                except ValueError:
                    error_message = 'ページ番号は数値で設定してください。'
                else:
                    page_number = int(page_number)

                if error_message:
                    context = {
                        'form': form,
                        'error_message': error_message,
                    }
                    
                    return render(request, 'imagetranscription/pdf.html', context)
                
                page_number -= 1
                
                output_filename = f"page{page_number}.jpg"
                output_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', output_filename)
                text, image_path = pdf_to_text(doc, output_path, page_number)
                image_url = settings.MEDIA_URL + '/pdfs/' + output_filename
                uploaded.delete()
                context = {
                    'form': form,
                    'result_text': text,
                    "image_url": image_url
                }
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