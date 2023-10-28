from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.db.models import Q, Count

from searchapp.models import Product
from board.models import Board

from signapp.models_bookmark import FBookmark
from signapp.models_bookmark import BBookmark
try:
    from searchapp.collarbor import food_recommend
    from searchapp.collarbor import board_recommend
except:
    pass
# Create your views here.

class HomeView(TemplateView):
    template_name = 'mainapp/home.html'

class AboutView(TemplateView):
    template_name = 'mainapp/about.html'


def Collarbor(request):
    username = request.user
    fcollarbors = []
    bcollarbors = []
    ranks = []
    
    if not username.is_anonymous:
        fcollarbor_list = food_recommend(str(username)).keys()
        bcollarbor_list = board_recommend(str(username)).keys()

        for col in fcollarbor_list:
            collarbor = Product.objects.all().get(
                Q(prdlstReportNo__exact = col)
            )
            fcollarbors.append(collarbor)

        for col in bcollarbor_list:
            collarbor = Board.objects.all().get(
                Q(bno__exact = col)
            )
            bcollarbors.append(collarbor)
    else:
        counts = {}
        fblist = FBookmark.objects.values('FNO')

        for fno in fblist:
            if fno['FNO'] in ranks:
                counts[fno['FNO']] += 1
            else:
                counts[fno['FNO']] = 1

        counts = sorted(counts.items(), reverse=True, key=lambda x:x[1])[:5]

        for fno in counts:
            rank_list = Product.objects.all().get(
                Q(prdlstReportNo__exact = fno[0])
            )
            ranks.append(rank_list)

    # print(fcollarbors)
    # print(bcollarbors)
    # print(ranks)

    return render(request, 'mainapp/home.html', {'fcollarbors':fcollarbors, 'bcollarbors':bcollarbors, 'ranks':ranks})