from django.db import models

# Create your models here.
class Board(models.Model):
    bno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    name = models.CharField(max_length=8)
    # id 필드로 추가하여 변경할 예정
    # cno = models.ForeignKey("")
    cno = models.CharField(max_length=8)
    allerinfo = models.TextField(null=True)
    cdate = models.DateField()
    content = models.TextField()

    class Meta:
        db_table = "boards" # DB에 표시되고 사용할 테이블 명


class Comment(models.Model):
    serialno = models.AutoField(primary_key=True)
    # bno = models.CharField(max_length=8)
    bno = models.ForeignKey("Board", related_name="board", on_delete=models.CASCADE, db_column="bno")
    # id 필드로 추가하여 변경할 예정
    # cno = models.ForeignKey("")
    cno = models.CharField(max_length=8)
    cdate = models.DateField()

    class Meta:
        db_table = "comments" # DB에 표시되고 사용할 테이블 명