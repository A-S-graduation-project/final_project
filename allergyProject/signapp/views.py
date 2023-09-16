from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from signapp.models import Customer
from signapp.forms import SignupForm, LoginForm
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

# 사용자 로그인 뷰
class UserLoginView(View):
    template_name = 'signapp/login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            try:
                customer = Customer.objects.get(username=username)
                if customer.password == password:
                    # 로그인 성공
                    request.session['customer_id'] = customer.cno
                    # 로그인 성공 시 홈 페이지로 리디렉션
                    return redirect(reverse('main:home'))
                else:
                    # 비밀번호가 일치하지 않음
                    error_msg = '비밀번호가 틀렸습니다'
            except Customer.DoesNotExist:
                # 해당 사용자가 존재하지 않음
                error_msg = '존재하지 않는 ID입니다'
        else:
            # 폼 유효성 검사 실패 시 에러 메시지 반환
            error_msg = '입력값이 올바르지 않습니다'
        return render(request, self.template_name, {'form': form, 'error_msg': error_msg})

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
