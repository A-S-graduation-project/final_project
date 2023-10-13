from django import forms
from django.forms import ModelForm
from .models import Board, Comment, BoardImage
import json


# 재료를 담을 form을 생성
class IngredientForm(forms.Form):
    ingredient_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "재료명"}))
    quantity = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={"placeholder": "수량"}))
    unit = forms.CharField(max_length=20, widget=forms.TextInput(attrs={"placeholder": "단위"}))

# ModelForm으로 BoardForm 클래스 생성
class BoardForm(ModelForm):
    # ingredient = forms.CharField(widget=forms.HiddenInput())
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': '레시피를 입력하세요'}))
    class Meta:
        # Board모델의 모든 필드를 사용하고
        model = Board
        fields = ['title', 'content']

        # 위젯으로 title과 content를 꾸밈
        widgets = {
            "title" : forms.TextInput(attrs={"placeholder": " 제목을 입력하세요"}),
            # "content" : forms.Textarea(attrs={"placeholder": " 레시피를 입력해주세요"}),
        }

    def clean_ingredient(self):
        data = self.cleaned_data.get('ingredient')
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                raise forms.ValidationError("잘못된 JSON 형식입니다.")
        return {}

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.ingredient = json.dumps(self.cleaned_data.get('ingredient'))
        if commit:
            instance.save()
        return instance

# board의 이미지를 넣기 위함 form
class ImageForm(ModelForm):
    class Meta:
        model = BoardImage
        fields = ['image']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comments']