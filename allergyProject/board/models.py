from django.db import models
from django.db.models import JSONField
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Board(models.Model):
    bno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    name = models.CharField(max_length=8, null=True)
    cno = models.CharField(max_length=8, null=True)
    allerinfo = models.TextField(null=False)
    cdate = models.DateField()
    ingredient = JSONField(null=False)
    content = ArrayField(models.CharField(max_length=500), null=False)
    images = models.ManyToManyField('Image', blank=True)

    class Meta:
        db_table = "boards" # DB에 표시되고 사용할 테이블 명

class Image(models.Model):
    image = models.ImageField()

    class Meta:
        db_table = "images" # DB에 표시되고 사용할 테이블 명

class Comment(models.Model):
    serialno = models.AutoField(primary_key=True)
    bno = models.ForeignKey("Board", related_name="board", on_delete=models.CASCADE, db_column="bno")
    cno = models.CharField(max_length=8)
    cdate = models.DateField(blank=True, null=True)
    udate = models.DateField(blank=True, null=True)
    comments = models.CharField(max_length=500, null=True)

    class Meta:
        db_table = "comments" # DB에 표시되고 사용할 테이블 명
