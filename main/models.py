from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    name = models.CharField()
    yaratilgan_sanasi = models.DateField(auto_now_add=True)
    muallif = models.CharField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.CharField(null=True)
