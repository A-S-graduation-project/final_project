from django import forms
from .models import Customer
from django.contrib.auth.hashers import make_password 
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
class LoginForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['username', 'password'] # 로그인 시에는 유저이름과 비밀번호만 입력 받는다.

# 회원 가입을 위한 폼 정의
class SignupForm(forms.ModelForm):
    # gender 필드는 HiddenInput 위젯을 사용하여 숨겨진 필드로 정의되며 초기값은 1로 설정됩니다.
    gender = forms.IntegerField(widget=forms.HiddenInput(), initial=1)
    
    class Meta:
        model = Customer  # 폼과 연결될 모델
        fields = ['username', 'email', 'phone', 'birthdate', 'gender', 'password']  # 폼에 사용될 필드들
    
    # 비밀번호 확인용 필드를 PasswordInput 위젯으로 정의합니다.
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    
    # 비밀번호가 같은지 검사하는 메서드
    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")

        return password_confirm

    # 이메일 중복 검사를 위한 메서드
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # 이미 등록된 이메일이 존재하면 에러 발생
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError("이미 있는 이메일입니다.")
        
        return email
    
    # 아이디 중복 검사를 위한 메서드
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        # 이미 등록된 이메일이 존재하면 에러 발생
        if Customer.objects.filter(username=username).exists():
            raise forms.ValidationError("이미 있는 ID입니다.")
        
        return username
    
#회원 정보를 편집할수 있게 만든 form
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['email', 'phone', 'birthdate', 'gender', 'password']

    # 비밀번호 필드를 PasswordInput 위젯으로 설정
    password = forms.CharField(required=False, widget=forms.PasswordInput)
    # 이메일 필드를 선택적으로 만듦
    email = forms.EmailField(required=False)

def update_profile(request):
    if request.method == 'POST':
        user_profile = Customer.objects.get(username=request.user.username)
        form = UserProfileForm(request.POST, instance=user_profile)

        if form.is_valid():
            # 이메일과 비밀번호 필드를 가져와서 변경된 경우에만 업데이트
            new_email = form.cleaned_data['email']
            new_password = form.cleaned_data['password']

            if new_email != user_profile.email:
                user_profile.email = new_email
            if new_password:
                user_profile.password = make_password(new_password)

            user_profile.phone = form.cleaned_data['phone']
            user_profile.birthdate = form.cleaned_data['birthdate']
            user_profile.gender = form.cleaned_data['gender']

            user_profile.save()
            messages.success(request, '프로필이 성공적으로 업데이트되었습니다.')
            return redirect(reverse('signapp:mypage'))
        else:
            messages.error(request, '프로필 업데이트에 실패했습니다. 입력 값을 확인하세요.')
    else:
        user_profile = Customer.objects.get(username=request.user.username)
        form = UserProfileForm(instance=user_profile)

    context = {
        'user_profile': user_profile,
        'form': form,
    }
    return render(request, 'signapp/mypage.html', context)