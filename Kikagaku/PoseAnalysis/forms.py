from django import forms

class VideoUploadForm(forms.Form):
    media_file = forms.FileField(label='ファイルをアップロード')