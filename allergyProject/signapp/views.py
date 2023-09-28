from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView
from django.contrib import messages
from signapp.models import Customer
from signapp.forms import SignupForm, UserProfileForm, CustomUserChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.hashers import make_password 
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator

# 사용자 로그인 뷰
class UserLoginView(View):
    def get(self, request):
        # 로그인 폼을 보여주는 부분 (GET 요청)
        return render(request, 'signapp/login.html')
    
    def post(self, request):
        # POST 요청으로 로그인 정보를 처리
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # 로그인 성공
            login(request, user)
            return redirect('main:home')  # 로그인 후 홈페이지로 리디렉션
        else:
            error_message = '로그인에 실패하였습니다. 다시 시도해주세요.'
            messages.error(request, error_message)
            return render(request, 'signapp/login.html', {'error_message': error_message})

# 사용자 회원 가입 뷰
class SignupView(FormView):
    template_name = 'signapp/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('main:home')

    def form_valid(self, form):
        # 비밀번호를 해싱하여 저장
        user = form.save(commit=False)
        user.password = make_password(form.cleaned_data['password'])
        user.save()

        # 사용자를 로그인 시킴
        login(self.request, user)

        return super().form_valid(form)

# 사용자 마이페이지 뷰
@method_decorator(login_required, name='dispatch')
class MypageView(View):
    template_name = 'signapp/mypage.html'

    def get(self, request, *args, **kwargs):
        user_profile = Customer.objects.get(username=request.user.username)
        form = UserProfileForm(instance=user_profile)
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
        form = CustomUserChangeForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            return redirect('signapp:mypage')
        
    else:
        form = CustomUserChangeForm(instance = request.user)
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