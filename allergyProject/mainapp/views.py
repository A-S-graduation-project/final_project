from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.db.models import Q

from searchapp.models import Product
try:
    from searchapp.collarbor import food_recommend
except:
    pass
# Create your views here.

class HomeView(TemplateView):
    template_name = 'mainapp/home.html'

class AboutView(TemplateView):
    template_name = 'mainapp/about.html'


def Collarbor(request):
    username = request.user
    collarbor_list = []
    collarbors = []
    
    if not username.is_anonymous:
        collarbor_list = food_recommend(str(username)).keys()

    for col in collarbor_list:
        collarbor = Product.objects.all().get(
            Q(prdlstReportNo__exact = col)
        )
        collarbors.append(collarbor)

    # print(collarbors)

    return render(request, 'mainapp/home.html', {'collarbors':collarbors})