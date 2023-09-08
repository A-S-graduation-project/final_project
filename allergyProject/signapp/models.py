from django.db import models

# Create your models here.
class Customer(models.Model):
    cno = models.AutoField(primary_key=True)
    username = models.CharField(max_length=8)
    email = models.CharField(max_length=20)
    phone = models.CharField(max_length=16)
    birthdate = models.DateField()
    gender = models.BooleanField()
    password = models.CharField(max_length=20)
    bookinfo = models.TextField(null=True)
    boardinfo = models.TextField(null=True)