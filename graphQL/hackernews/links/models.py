from django.db import models


# Create your models here.
class Link(models.Model):
    url = models.URLField()
    description = models.TextField(null=False, blank=True)