# 사용자 마이페이지 뷰
from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, update_session_auth_hash
from django.urls import reverse_lazy

from signapp.models import Customer
from .forms import forms_CustomerUserChangeForm, forms_UserProfileForm


@method_decorator(login_required, name='dispatch')
class MypageView(View):
    template_name = 'signapp/mypage.html'

    def get(self, request, *args, **kwargs):
        user_profile = Customer.objects.get(username=request.user.username)
        allerinfo_str = user_profile.allerinfo
        allerinfo_list = [int(item) for item in allerinfo_str.strip('[]').split(',')]
        form = forms_UserProfileForm.UserProfileForm(instance=user_profile,initial={'allerinfo': allerinfo_list})
        context = {
            'user_profile': user_profile,
            'form': form,
        }
        return render(request, self.template_name, context)
        
class UserLogoutView(LogoutView):
    # 로그아웃 후 리디렉션할 URL 설정
    next_page = reverse_lazy('main:home')

def delete(request):
    user = request.user
    user.delete()
    return redirect("signapp:login")

def update(request):
    if request.method == "POST":
        form = forms_CustomerUserChangeForm.CustomUserChangeForm(request.POST, instance = request.user)
        if form.is_valid():
            user = form.save(commit=False)
            allergies = form.cleaned_data.get('allerinfo')
            selected_allergies = [allergy.ano for allergy in allergies]

            # 사용자 프로필의 allerinfo 필드에 저장
            user.allerinfo = selected_allergies
            user.save()
            return redirect('signapp:mypage')
        
    else:
        form = forms_CustomerUserChangeForm.CustomUserChangeForm(instance = request.user)
    context = {'form':form}
    return render(request, 'signapp/mypage.html', context)

def update_password(request):
    if request.method == "POST":
        # POST 요청에서 폼 데이터 추출
        new_password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        # 새 비밀번호와 비밀번호 확인이 일치하는지 확인
        if new_password != password_confirm:
            messages.error(request, '새 비밀번호와 비밀번호 확인이 일치하지 않습니다.')
            return redirect('signapp:mypage')  # 변경 페이지로 리디렉션

        # 비밀번호 변경
        user = request.user
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)  # 세션 업데이트
        
        # 사용자 로그아웃
        logout(request)

        messages.success(request, '비밀번호가 성공적으로 변경되었습니다.')
        return redirect('signapp:login')  # 변경 페이지로 리디렉션

    return render(request, 'signapp/mypage.html')