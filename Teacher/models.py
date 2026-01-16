from django.db import models
from django.utils import timezone
from django.shortcuts import render
from django.db.models import Q
# Create your models here.


# Section ------------------------------------------------
class Section(models.Model):
    name = models.CharField(max_length=50)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.year})"
