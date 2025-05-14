from django.shortcuts import render
from django.conf import settings
from django.http import FileResponse, Http404
from .forms import VideoUploadForm
from .poseestimate import estimate_video_pose, estimate_image_pose, convert_to_h264
import os
import uuid

def index(request):
    if request.method == 'POST':
        error_message = None
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            media_file = request.FILES['media_file']
            image_extensions = ['.jpeg', '.jpg', '.png']
            video_extensions = ['.mp4', '.mov', '.avi', '.mkv']
            ext = os.path.splitext(media_file.name)[1].lower()
            if ext in image_extensions:
                temp_path = os.path.join(settings.MEDIA_ROOT, 'temp_img.jpg')
                with open(temp_path, 'wb+') as f:
                    for chunk in media_file.chunks():
                        f.write(chunk)

                base64_img = estimate_image_pose(temp_path)
                os.remove(temp_path)

                context = {
                    'form': form,
                    'error_message': None,
                    'image_type': 'image/jpeg',
                    'image': base64_img,
                }
                return render(request, 'poseanalysis/index.html', context)
            
            elif ext in video_extensions:
                fps_rate = request.POST['fps_rate']
                try:
                    float(fps_rate)
                    if float(fps_rate) < 0.5 or float(fps_rate) > 2:
                        error_message = '速度倍率は0.5〜2の範囲で設定してください。'
                except ValueError:
                    error_message = '速度倍率は数値で設定してください。'
                else:
                    fps_rate = float(fps_rate)

                if error_message:
                    context = {
                        'form': form,
                        'error_message': error_message,
                    }
                    return render(request, 'poseanalysis/index.html', context)
            
                video_filename = os.path.splitext(media_file.name)[0]
                input_filename = f"{uuid.uuid4()}.mp4"
                input_path = os.path.join(settings.MEDIA_ROOT, input_filename)

                with open(input_path, 'wb+') as f:
                    for chunk in media_file.chunks():
                        f.write(chunk)

                process_filename = f'processed_{input_filename}'
                output_filename = f'movies/{process_filename }'
                output_path = os.path.join(settings.MEDIA_ROOT, output_filename)

                temp_filename = f'movies/temp_processed_{input_filename}'
                temp_path = os.path.join(settings.MEDIA_ROOT, temp_filename)

                estimate_video_pose(input_path, temp_path, fps_rate)
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
                error_message = '画像または動画ファイルをアップロードしてください \n 画像は「jpg, pngファイル」、 動画は「mp4, mov, avi, mkv」ファイルが使用できます'
                context = {
                    'form': form,
                    'error_message': error_message,
                }
                return render(request, 'poseanalysis/index.html', context)
        else:
            error_message = "不明なエラーが発生しました。"
            context = {
                    'form': form,
                    'error_message': error_message,
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