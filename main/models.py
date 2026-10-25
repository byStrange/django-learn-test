from os import name
from statistics import mode

from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    name = models.CharField()
    yaratilgan_sanasi = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.CharField(null=True)
    public = models.BooleanField(default=False)

class BookView(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
