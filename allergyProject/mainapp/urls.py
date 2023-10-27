from django.urls import path
from .views import HomeView, AboutView
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.Collarbor, name='collarbor'),
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
]

