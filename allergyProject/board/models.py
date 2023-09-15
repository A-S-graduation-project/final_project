from django.db import models
from django.db.models import JSONField
import json

class JSONListField(models.TextField):
    def from_db_value(self, value, expression, connection):
        if not value:
            return []
        try:
            return json.loads(value)
        except (TypeError, ValueError):
            return []

    def to_python(self, value):
        if not value:
            return []
        if isinstance(value, list):
            return value
        try:
            return json.loads(value)
        except (TypeError, ValueError):
            return []

    def get_prep_value(self, value):
        if not value:
            return "[]"
        if isinstance(value, str):
            return value
        return json.dumps(value)
    
class Recipe(models.Model):
    recipe = JSONListField()

    class Meta:
        db_table = "Recipes" # DB에 표시되고 사용할 테이블 명

# Create your models here.
class Board(models.Model):
    bno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    name = models.CharField(max_length=8)
    # id 필드로 추가하여 변경할 예정
    cno = models.CharField(max_length=8)
    allerinfo = models.TextField(null=True)
    cdate = models.DateField()
    ingredient = JSONListField()
    content = models.OneToOneField(Recipe, on_delete=models.CASCADE)

    class Meta:
        db_table = "boards" # DB에 표시되고 사용할 테이블 명

class Comment(models.Model):
    serialno = models.AutoField(primary_key=True)
    # bno = models.CharField(max_length=8)
    bno = models.ForeignKey("Board", related_name="board", on_delete=models.CASCADE, db_column="bno")
    # id 필드로 추가하여 변경할 예정
    cno = models.CharField(max_length=8)
    cdate = models.DateField()

    class Meta:
        db_table = "comments" # DB에 표시되고 사용할 테이블 명
