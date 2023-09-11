from django.db import models

# Create your models here.
class Customer(models.Model):
    cno = models.CharField(max_length=8, primary_key=True)
    username = models.CharField(max_length=8)
    email = models.EmailField(max_length=40, unique=True)
    phone = models.CharField(max_length=16)
    password = models.CharField(max_length=20)
    birthdate = models.DateField()
    gender = models.BooleanField()
    bookinfo = models.TextField(blank=True, null=True)
    boardinfo = models.TextField(blank=True, null=True)