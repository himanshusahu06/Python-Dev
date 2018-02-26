from django.db import models
from django.contrib.auth.models import AbstractUser

import binascii
import os

# Create your models here.
class User(AbstractUser):
    token = models.CharField(max_length=40)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = binascii.hexlify(os.urandom(20)).decode()
        return super().save(*args, **kwargs)
