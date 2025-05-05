from django import forms


class ImageUploadForm(forms.Form):
    image = forms.FileField(label="画像をアップロード")