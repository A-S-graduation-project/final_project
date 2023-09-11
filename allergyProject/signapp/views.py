from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from signapp.models import Customer
from signapp.forms import SignupForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

# 사용자 로그인 뷰
class UserLoginView(View):
    template_name = 'signapp/login.html'  # 로그인 템플릿 경로

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            print('로그인 성공:', email)
            return redirect('mainapp:homr')  # 로그인 성공 시 리다이렉트할 URL 설정
        else:
            error = "이메일 또는 비밀번호가 일치하지 않습니다."
            print('로그인 실패:', email, password)
            return render(request, self.template_name, {'error': error})

# 사용자 회원 가입 뷰
class SignupView(SuccessMessageMixin, CreateView):
    model = Customer
    form_class = SignupForm
    template_name = 'signapp/signup.html'
    success_url = reverse_lazy('signapp:login')
    success_message = "회원 가입이 완료되었습니다."

    # 폼 데이터가 유효할 때 실행되는 메서드
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
    
    # 폼 데이터가 유효하지 않을 때 실행되는 메서드
    def form_invalid(self, form):
        return super().form_invalid(form)

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
