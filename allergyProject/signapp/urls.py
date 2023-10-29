from django.urls import path
from . import views_bookmark
from . import views_mypage
from . import views_myboard
from . import views_signup
from . import views_userloginview
app_name = 'signapp'

urlpatterns = [
    path('login/', views_userloginview.UserLoginView.as_view() , name='login'),
    path('signup/', views_signup.SignupView.as_view() , name='signup'), # 회원 가입 URL 패턴
    path('mypage/', views_mypage.MypageView.as_view() , name='mypage'),
    path('logout/', views_mypage.UserLogoutView.as_view(), name='logout'), # 로그아웃 URL
    path('delete/', views_mypage.delete, name='delete'),
    path('update/', views_mypage.update, name='update'),
    path('update_password/', views_mypage.update_password, name = 'update_password'),
    path('bookmarks/', views_bookmark.bookmarks, name='bookmarks'),
    path('delete_fbookmark/', views_bookmark.delete_fbookmark, name='delete_fbookmark'),
    path('delete_bbookmark/', views_bookmark.delete_bbookmark, name='delete_bbookmark'),
    path('delete_board/', views_myboard.delete_board, name='delete_board'),
    path('myboard/', views_myboard.my_board, name='my_board'),
]