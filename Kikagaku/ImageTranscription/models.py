from django.db import models
import os

class UploadImage(models.Model):
    image = models.ImageField(upload_to='images/')

    def delete(self, *args, **kwargs):
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)