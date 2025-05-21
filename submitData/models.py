from django.db import models
from django.utils import timezone

class UserPass(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
