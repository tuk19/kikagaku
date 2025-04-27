from django import forms
from django.forms import ModelForm
from .models import UploadImage, UploadPDF

# class ImageUploadForm(forms.Form):
#     image = forms.ImageField(label="画像をアップロード")

class ImageUploadForm(ModelForm):
    class Meta:
        model = UploadImage
        fields = {'image'}

class PDFUploadForm(ModelForm):
    class Meta:
        model = UploadPDF
        fields = {'pdf'}