from django.shortcuts import render
from .forms import MusicUploadForm

def index(request):
    if request.method == "POST":
        form = MusicUploadForm(request.POST, request.FILES)
        if form.is_valid():
            music = form.cleaned_data['music']
            context = {
                'form': form,
                'music': music,
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
