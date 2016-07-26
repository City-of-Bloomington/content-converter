from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=200)

    #a url safe version of the name
    tag = models.CharField(max_length=200)

    #the default path prefix for the alias:
    base = models.CharField(max_length=200)

    #optional field
    parent = models.ForeignKey('self', blank=True, null=True)

