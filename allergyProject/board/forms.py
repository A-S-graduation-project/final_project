from django import forms
from django.forms import ModelForm
from .models import Board, Comment, BoardImage
import json


# ModelForm으로 BoardForm 클래스 생성
class BoardForm(ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': '레시피를 입력하세요'}))
    ingredient = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "ex) 돼지고기 300g"}))
    class Meta:
        # Board모델의 모든 필드를 사용하고
        model = Board
        fields = ['title', 'ingredient', 'content']

        # 위젯으로 title과 content를 꾸밈
        widgets = {
            "title" : forms.TextInput(attrs={"placeholder": " 제목을 입력하세요"}),
        }

# board의 이미지를 넣기 위함 form
class ImageForm(ModelForm):
    class Meta:
        model = BoardImage
        fields = ['image']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comments']

        widgets = {
            "comments" : forms.Textarea(attrs={"placeholder": "댓글을 남겨주세요"})
        }