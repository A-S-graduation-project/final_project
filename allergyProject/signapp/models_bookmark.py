from datetime import date
from django.db import models
from searchapp.models import Product  # searchapp 애플리케이션의 Product 모델을 임포트합니다.
from board.models import Board  # board 애플리케이션의 Board 모델을 임포트합니다.
from signapp.models import Customer  # signapp 애플리케이션의 Customer 모델을 임포트합니다.

class FBookmark(models.Model):
    FMNO = models.AutoField(primary_key=True)
    TITLE = models.CharField(max_length=100, null=False)
    CNO = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Customer 모델과의 관계 설정
    FNO = models.ForeignKey(Product, on_delete=models.CASCADE)    # Product 모델과의 관계 설정
    CDATE = models.DateField(null=False, default=date.today)
    
    class Meta: 
        db_table = "fbookmark" 
            
class BBookmark(models.Model):
    BMNO = models.AutoField(primary_key=True)
    TITLE = models.CharField(max_length=100, null=False)
    CNO = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Customer 모델과의 관계 설정
    bNO = models.ForeignKey(Board, on_delete=models.CASCADE)    # Board 모델과의 관계 설정
    CDATE = models.DateField(null=False, default=date.today)
    
    class Meta: 
        db_table = "bbookmark"