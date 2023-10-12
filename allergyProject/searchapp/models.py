from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
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
    
    class Meta:
        db_table = "products" # DB에 표시되고 사용할 테이블 명


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
    
    class Meta:
        db_table = "userdata" # DB에 표시되고 사용할 테이블 명
    

# allergy category table 작성 필요 #
class Allergy(models.Model):
    ano = models.AutoField(primary_key=True)
    allergy = models.CharField(max_length=45, unique=True)

    class Meta:
        db_table = "allergies" # DB에 표시되고 사용할 테이블 명


class PSimilarity(models.Model):
    prdNo = models.CharField(max_length=50, primary_key=True)
    simlist = ArrayField(models.CharField(max_length=50), null=True)

    class Meta:
        db_table = "psimilarity" # DB에 표시되고 사용할 테이블 명


class Recommend(models.Model):
    serialno = models.AutoField(primary_key=True)
    cno = models.IntegerField()
    rno = models.CharField(max_length=50)

    class Meta:
        db_table = "recommend" # DB에 표시되고 사용할 테이블 명