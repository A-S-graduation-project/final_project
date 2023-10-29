from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.views import View
from django.contrib import messages
from django.contrib.auth import login

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