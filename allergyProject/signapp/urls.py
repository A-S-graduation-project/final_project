from django.urls import path
from . import views as signviews

app_name = 'signapp'

urlpatterns = [
    path('login/', signviews.Login, name='login'),
    path('signup/', signviews.Signup , name='signup'),
    path('mypage/', signviews.Mypage, name='mypage'),

]
