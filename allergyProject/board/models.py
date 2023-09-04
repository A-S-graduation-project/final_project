from django.db import models

# Create your models here.
class Board(models.Model):
    bno = models.CharField(max_length=8, primary_key=True)
    title = models.CharField(max_length=100)
    name = models.CharField(max_length=8)
    cno = models.CharField(max_length=8)
    allerinfo = models.TextField(null=True)
    cdate = models.DateField()
    content = models.TextField()

class Comment(models.Model):
    serialno = models.CharField(max_length=10, primary_key=True)
    # bno = models.CharField(max_length=8)
    bno = models.ForeignKey("Board", related_name="board", on_delete=models.CASCADE, db_column="bno")
    cno = models.CharField(max_length=8)
    cdate = models.DateField()