from django import forms

class ImageUploadForm(forms.Form):
    image = forms.ImageField(label="画像をアップロード")


# from django import forms

# class ImageUploadform(forms.Form):
#     image = forms.ImageField(label="画像をアップロード")