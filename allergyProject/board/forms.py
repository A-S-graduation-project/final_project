from django import forms
from django.forms import ModelForm
from .models import Board, Recipe
import json

# ModelForm으로 BoardForm 클래스 생성
class BoardForm(ModelForm):
    class Meta:
        # Board모델의 모든 필드를 사용하고
        model = Board
        fields = "__all__"

        # 위젯으로 title과 content를 꾸밈
        widgets = {
            "title" : forms.TextInput(attrs={"placeholder": "제목을 입력하세요"}),
            # "content": forms.Textarea(attrs={"placeholder": "레시피를 알려주세요"})
        }

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = "__all__"
        widgets = {
            "recipe" : forms.Textarea(attrs={"placeholder": "레시피를 알려주세요"})
        }