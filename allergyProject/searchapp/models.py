from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
# Create your models here.

class Product(models.Model):
    prdlstReportNo = models.CharField(primary_key=True, max_length=50)
    prdlstNm = models.CharField(max_length=200)
    rawmtrl = models.TextField()
    allergy = models.TextField(null=True)
    manufacture = models.CharField(max_length=200, null=True)
    prdkind = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.prdlstNm

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class UserData(models.Model):
    rnum = models.AutoField(primary_key=True)
    gender = models.BooleanField(null=True)
    older = models.IntegerField(null=True)
    allergy = models.TextField()
    prdlstReportNo = models.CharField(max_length=20)
    prdlstNm = models.CharField(max_length=200)
    rating = models.IntegerField()

    def __str__(self):
        return self.allergy