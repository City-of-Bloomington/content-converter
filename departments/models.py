from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Department(models.Model):
    """
    """
    name = models.CharField(max_length=200)
    #safe for url:
    tag = models.CharField(max_length=200, default='')
    
    def __str__(self):
        return self.name
