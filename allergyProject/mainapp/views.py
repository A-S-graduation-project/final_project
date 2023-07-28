from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

# Create your views here.

class HomeView(TemplateView):
    template_name = 'mainapp/home.html'

class AboutView(TemplateView):
    template_name = 'mainapp/about.html'