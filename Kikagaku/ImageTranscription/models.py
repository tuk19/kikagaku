from django.db import models
from django.core.exceptions import ValidationError
import os


def validate_pdf(file):
    if not file.name.lower().endswith('.pdf'):
        raise ValidationError('PDFファイルのみアップロードできます')


class UploadImage(models.Model):
    image = models.ImageField(upload_to='images/')

    def delete(self, *args, **kwargs):
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)


class UploadPDF(models.Model):
    pdf = models.FileField(upload_to='pdfs/', validators=[validate_pdf])

    def delete(self, *args, **kwargs):
        if self.pdf and os.path.isfile(self.pdf.path):
            os.remove(self.pdf.path)
        super().delete(*args, **kwargs)