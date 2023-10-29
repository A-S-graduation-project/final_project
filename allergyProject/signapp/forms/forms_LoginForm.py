from django import forms
from signapp.models import Customer

class LoginForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['username', 'password'] # 로그인 시에는 유저이름과 비밀번호만 입력 받는다.