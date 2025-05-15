from django import forms

class MusicUploadForm(forms.Form):
    music = forms.FileField(label="音楽ファイルをアップロード")

    def clean_music(self):
        file = self.cleaned_data['music']
        if not file.name.endswith(('.wav', '.mp3', '.m4a')):
            raise forms.ValidationError('MP3、WAV、M4Aいずれかのファイルのみアップロードできます')
        return file