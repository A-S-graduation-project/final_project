from django.urls import path
from .views import BoardView
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'board'

urlpatterns = [
    path('', BoardView.as_view(), name='board_list'),
    path('board_create/', views.create_board, name='board_create'),
    path('board_detail/<int:bno>', views.read_board, name="board_detail"),
    path('board_detail/<int:bno>/delete', views.delete_board, name='delete_board'),
    path('board_detail/<int:bno>/create_comment', views.create_comment, name='create_comment'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)