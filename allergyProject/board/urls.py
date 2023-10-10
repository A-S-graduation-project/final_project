from django.urls import path
from .views import BoardView
from . import views

app_name = 'board'

urlpatterns = [
    path('', BoardView.as_view(), name='board_list'),
    path('board_create/', views.create_board, name='board_create'),
    path('board_detail/<int:bno>', views.read_board, name="board_detail"),
    path('board_detail/<int:bno>/delete', views.delete_board, name='delete_board'),
]