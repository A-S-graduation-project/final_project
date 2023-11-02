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
    path('board_detail/<int:bno>/update', views.update_board, name='update_board'),
    path('board_detail/<int:bno>/delete', views.delete_board, name='delete_board'),
    path('board_detail/<int:bno>/create_comment', views.create_comment, name='create_comment'),
    path('board_detail/<int:bno>/update_comment/<int:serialno>', views.update_comment, name='update_comment'),
    path('board_detail/<int:bno>/delete_comment/<int:serialno>', views.delete_comment, name='delete_comment'),
    path('like_button/', view_add_board.like_button_view, name='like_button'),
]