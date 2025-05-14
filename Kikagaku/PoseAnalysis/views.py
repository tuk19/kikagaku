from django.shortcuts import render
from django.conf import settings
from django.http import FileResponse, Http404
from .forms import VideoUploadForm
from .poseestimate import estimate_pose, convert_to_h264
import os
import uuid

def index(request):
    if request.method == 'POST':
        error_state = False
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video_file = request.FILES['video_file']
            fps_rate = request.POST['fps_rate']
            try:
                float(fps_rate)
                if float(fps_rate) < 0.5 or float(fps_rate) > 2:
                    error_message = '速度倍率は0.5〜2の範囲で設定してください。'
                    error_state = True
            except ValueError:
                error_message = '速度倍率は数値で設定してください。'
                error_state = True
            else:
                fps_rate = float(fps_rate)

            if error_state:
                context = {
                    'form': form,
                    'error_message': error_message,
                }
                return render(request, 'poseanalysis/index.html', context)

            valid_extensions = ['.mp4', '.mov', '.avi', '.mkv']
            ext = os.path.splitext(video_file.name)[1].lower()
            if ext not in valid_extensions:
                error_message = '動画ファイルをアップロードしてください \n mp4, mov, avi, mkv ファイルが使用できます'
                context = {
                    'form': form,
                    'error_message': error_message,
                }
                return render(request, 'poseanalysis/index.html', context)

            video_filename = os.path.splitext(video_file.name)[0]
            input_filename = f"{uuid.uuid4()}.mp4"
            input_path = os.path.join(settings.MEDIA_ROOT, input_filename)

            with open(input_path, 'wb+') as f:
                for chunk in video_file.chunks():
                    f.write(chunk)

            process_filename = f'processed_{input_filename}'
            output_filename = f'movies/{process_filename }'
            output_path = os.path.join(settings.MEDIA_ROOT, output_filename)

            temp_filename = f'movies/temp_processed_{input_filename}'
            temp_path = os.path.join(settings.MEDIA_ROOT, temp_filename)

            estimate_pose(input_path, temp_path, fps_rate)
            convert_to_h264(temp_path, output_path)

            os.remove(input_path)
            os.remove(temp_path)

            filename = f'{video_filename}_{fps_rate}fps.mp4'
            video_url = settings.MEDIA_URL + output_filename
            
            context = {
                'form': form,
                'error_message': None,
                'video_url': video_url,
                'output_filename': process_filename,
                'download_filename': filename,
            }

            return render(request, 'poseanalysis/index.html', context)

    else:
        form = VideoUploadForm()
        context = {
            'form': form,
        }
    return render(request, 'poseanalysis/index.html', context)

def download_video(request, filename):
    output_filename = f'movies/{filename}'
    output_path = os.path.join(settings.MEDIA_ROOT, output_filename)
    if not os.path.exists(output_path):
        raise Http404("ファイルが存在しません")
    
    download_filename = os.path.basename(request.GET.get('name', filename))
    response = FileResponse(open(output_path, 'rb'), as_attachment=True, filename=download_filename)
    return response