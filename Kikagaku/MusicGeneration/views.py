from django.shortcuts import render
from django.conf import settings
from .generate_music import (
    load_model,
    generate_tokens,
    decode_tokens_to_midi,
    midi_to_audio,
    midi_to_image
)
import uuid
import os

def index(request):
    context = ""
    if request.method == "POST":
        midi_filename = f"{uuid.uuid4()}.mid"
        midi_path = os.path.join(settings.MEDIA_ROOT, 'audio', 'generate', midi_filename)
        wav_filename = midi_filename.replace('.mid', '.wav')
        wav_path = os.path.join(settings.MEDIA_ROOT, 'audio', 'generate', wav_filename)
        wav_url = os.path.join(settings.MEDIA_URL, 'audio/generate/', wav_filename)
        model = load_model()
        tokens = generate_tokens(model, max_length=2048)
        decode_tokens_to_midi(tokens, midi_path)
        midi_to_audio(midi_path, wav_path)
        image_base64, format = midi_to_image(midi_path)
        # midiファイルを保存するためコメントアウト
        # os.remove(midi_path)

        message = "楽曲生成しました"
        context = {
            'message': message,
            'wav_url': wav_url,
            'image': image_base64,
            'format': format,
        }
        return render(request, 'musicgeneration/index.html', context)
    else:
        return render(request, 'musicgeneration/index.html')