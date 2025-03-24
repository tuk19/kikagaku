from django.shortcuts import render
from .forms import ImageUploadform

def index(request):
    if request.method == "POST":
        form = ImageUploadform(request.POST, request.FILES)
        if form.is_valid():
            image = request.FILES['image']
            context = {
                'form': form,
                'image': image
            }
            return render(request, 'imageclassification/index.html', context)
    else:
        form = ImageUploadform()
        context = {
            'form': form,
        }

    return render(request, 'imageclassification/index.html', context)
