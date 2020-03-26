from django.db import models

# Create your models here.
class FBFileSchedularModel(models.Model):
    file_field = models.FileField(upload_to='facebook/')

    url_field = models.URLField(default="",blank=True)
    text_field = models.CharField(blank=True,max_length=200)
