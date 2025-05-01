from django.shortcuts import render
from django.conf import settings
from django.http import FileResponse
from .forms import VideoUploadForm
from .poseestimate import estimate_pose
import os
import uuid

def index(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video_file = request.FILES['video_file']

            valid_extensions = ['.mp4', '.mov', '.avi', '.mkv']
            ext = os.path.splitext(video_file.name)[1].lower()
            if ext not in valid_extensions:
                error_message = '動画ファイルをアップロードしてください \n mp4, mov, avi, mkv ファイルが使用できます'
                context = {
                    'form': form,
                    'error_message': error_message,
                }
                return render(request, 'poseanalysis/index.html', context)

            input_filename = f"{uuid.uuid4()}.mp4"
            input_path = os.path.join(settings.MEDIA_ROOT, input_filename)

            with open(input_path, 'wb+') as f:
                for chunk in video_file.chunks():
                    f.write(chunk)

            output_filename = f'processed_{input_filename}'
            output_path = os.path.join(settings.MEDIA_ROOT, output_filename)

            estimate_pose(input_path, output_path)
            os.remove(input_path)
            filename = 'processed_video.mp4'
            return FileResponse(open(output_path, 'rb'), as_attachment=True, filename=filename)

    else:
        form = VideoUploadForm()
        context = {
            'form': form,
        }
    return render(request, 'poseanalysis/index.html', context)