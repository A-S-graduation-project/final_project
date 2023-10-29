from django.urls import path
from . import views, view_add_board
from django.conf.urls.static import static
from django.conf import settings

app_name = 'board'

urlpatterns = [
    path('', views.board_view, name='board_list'),
    path('board_search/', views.board_search_result, name='board_search'),
    path('board_create/', views.create_board, name='board_create'),
    path('board_detail/<int:bno>', views.read_board, name="board_detail"),
    path('board_detail/<int:bno>/delete', views.delete_board, name='delete_board'),
    path('board_detail/<int:bno>/create_comment', views.create_comment, name='create_comment'),
    path('like_button/', view_add_board.like_button_view, name='like_button'),

]