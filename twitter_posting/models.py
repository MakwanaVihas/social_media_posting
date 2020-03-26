from django.db import models
from datetime import datetime

# Create your models here.
class FileSchedularModel(models.Model):
    file_field = models.FileField(upload_to='documents/',blank=True, null=True)
    schedule_time = models.DateTimeField(default=datetime.now)
    url_field = models.URLField(default="",blank=True)
    text_field = models.CharField(max_length=200)
