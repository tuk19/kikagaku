from django.shortcuts import render
from django.conf import settings
from .forms import MusicUploadForm
from .predict_music import predict_music

import uuid
import os

def index(request):
    if request.method == "POST":
        form = MusicUploadForm(request.POST, request.FILES)
        if form.is_valid():
            music = form.cleaned_data['music']
            input_filename = f"{uuid.uuid4()}.wav"
            input_path = os.path.join(settings.MEDIA_ROOT, input_filename)

            with open(input_path, 'wb+') as destination:
                for chunk in music.chunks():
                    destination.write(chunk)

            pred, pred_class = predict_music(input_path)

            context = {
                'form': form,
                'music': music,
                'pred': pred,
                'class': pred_class,
            }
            return render(request, 'musicclassification/index.html', context)
        else:
            context = {
                'form': form,
            }
            return render(request, 'musicclassification/index.html', context)
    else:
        form = MusicUploadForm()
        context = {
            'form': form,
        }
        return render(request, 'musicclassification/index.html', context)
