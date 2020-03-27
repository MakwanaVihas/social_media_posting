from django.db import models
from datetime import datetime

# Create your models here.
class InstaFileSchedular(models.Model):
    file_field = models.FileField(upload_to='instagram/',blank=True, null=True)
    schedule_time = models.DateTimeField(default=datetime.now)
    text_field = models.CharField(max_length=200)
