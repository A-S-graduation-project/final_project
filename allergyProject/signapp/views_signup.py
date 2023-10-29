from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import forms_SignupForm
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password 

# 사용자 회원 가입 뷰
class SignupView(FormView):
    template_name = 'signapp/signup.html'
    form_class = forms_SignupForm.SignupForm
    success_url = reverse_lazy('main:home')

    def form_valid(self, form):
        # 비밀번호를 해싱하여 저장
        user = form.save(commit=False)
        user.password = make_password(form.cleaned_data['password'])
        
        # 사용자 정보 저장
        allergies = form.cleaned_data.get('allerinfo')
        selected_allergies = [allergy.ano for allergy in allergies]

        # 사용자 프로필의 allerinfo 필드에 저장
        user.allerinfo = selected_allergies

        user.save()  # 사용자 정보 저장
        
        login(self.request, user)

        return super().form_valid(form)