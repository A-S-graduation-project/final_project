from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib import messages
from signapp.models import Customer
from signapp.forms import SignupForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password 
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

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
            print(username)
            print(password)
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

        messages.success(self.request, "회원 가입이 완료되었습니다.")
        return super().form_valid(form)

# 사용자 마이페이지 뷰
class MypageView(TemplateView):
    template_name = 'signapp/mypage.html'
    
    @method_decorator(login_required)  # 로그인 상태를 확인하는 데코레이터 적용
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    # 템플릿 컨텍스트 데이터 설정
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = Customer.objects.get(user=self.request.user)  # 현재 로그인한 사용자의 프로필 정보를 가져옴
        context['user_profile'] = user_profile
        return context
