from django import forms

class VideoUploadForm(forms.Form):
    video_file = forms.FileField(label='動画をアップロード')