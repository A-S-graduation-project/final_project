from django.urls import path
from . import views 
from . import view_add_bookmark

app_name = 'searchapp'

urlpatterns = [
    path('', views.searchResult, name='searchResult'),
    path('search_detail/', views.Detail, name='Detail'),
    path('like_button/', view_add_bookmark.like_button_view, name='like_button'),
]

