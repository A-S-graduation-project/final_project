from django.db import models
from django.db.models import JSONField
from django.contrib.postgres.fields import ArrayField
import os

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
    types = models.TextField(null=False)
    meterial = models.TextField(null=False)

    class Meta:
        db_table = "boards" # DB에 표시되고 사용할 테이블 명


def get_image_filename(instance, filename):
    # 이미지 파일의 원래 이름
    original_filename = os.path.basename(filename)
    
    # 이미지 파일의 새 이름 생성 (게시판 번호 + 원래 파일 이름)
    new_filename = f"bno_{instance.bno}_{original_filename}"
    
    # 반환하려는 파일 경로와 이름
    return os.path.join("", new_filename)

class BoardImage(models.Model):
    serial = models.AutoField(primary_key=True)
    bno = models.ForeignKey(Board, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_filename)

    class Meta:
        db_table = "board_images" # DB에 표시되고 사용할 테이블 명

class TypeCategories(models.Model):
    types = models.CharField(max_length=50)

    class Meta:
        db_table = "type_categories" # DB에 표시되고 사용할 테이블 명

class MeterialCategories(models.Model):
    materials = models.CharField(max_length=50)

    class Meta:
        db_table = "meterial_categories" # DB에 표시되고 사용할 테이블 명

class Comment(models.Model):
    serialno = models.AutoField(primary_key=True)
    bno = models.ForeignKey("Board", related_name="board", on_delete=models.CASCADE, db_column="bno")
    cno = models.CharField(max_length=8)
    cdate = models.DateField(blank=True, null=True)
    udate = models.DateField(blank=True, null=True)
    comments = models.CharField(max_length=500, null=True)

    class Meta:
        db_table = "comments" # DB에 표시되고 사용할 테이블 명


class BSimilarity(models.Model):
    bno = models.IntegerField(primary_key=True)
    simlist = ArrayField(models.IntegerField(), null=True)

    class Meta:
        db_table = "bsimilarity" # DB에 표시되고 사용할 테이블 명