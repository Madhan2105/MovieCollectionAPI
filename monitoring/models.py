from django.db import models


# Create your models here.
class Counter(models.Model):
    request_count = models.IntegerField(default=0)
    reset_count = models.IntegerField(default=0)
