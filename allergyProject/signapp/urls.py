from django.urls import path
from .views import UserLoginView, SignupView ,MypageView, UserLogoutView
from . import views
from . import views_bookmark
from .views_myboard import my_board
app_name = 'signapp'

urlpatterns = [
    path('login/', UserLoginView.as_view() , name='login'),
    path('signup/', SignupView.as_view() , name='signup'), # 회원 가입 URL 패턴
    path('mypage/', MypageView.as_view() , name='mypage'),
    path('logout/', UserLogoutView.as_view(), name='logout'), # 로그아웃 URL
    path('delete/', views.delete, name='delete'),
    path('update/', views.update, name='update'),
    path('update_password/', views.update_password, name = 'update_password'),
    path('bookmarks/', views_bookmark.bookmarks, name='bookmarks'),
    path('delete_fbookmark/', views_bookmark.delete_fbookmark, name='delete_fbookmark'),
    path('delete_bbookmark/', views_bookmark.delete_bbookmark, name='delete_bbookmark'),
    path('myboard/', my_board, name='my_board'),
]