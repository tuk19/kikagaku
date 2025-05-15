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
            music_filename = os.path.splitext(music.name)[0]
            input_filename = f"{uuid.uuid4()}.wav"
            input_path = os.path.join(settings.MEDIA_ROOT, 'audio', input_filename)

            with open(input_path, 'wb+') as destination:
                for chunk in music.chunks():
                    destination.write(chunk)

            pred, pred_class = predict_music(input_path)

            audio_url = os.path.join(settings.MEDIA_URL, 'audio', input_filename)

            context = {
                'form': form,
                'audio_url': audio_url,
                'audio_name': music_filename,
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
