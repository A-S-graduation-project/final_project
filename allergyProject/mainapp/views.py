from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.db.models import Q, Count

from searchapp.models import Product
from board.models import Board, BoardImage

try:
    from signapp.models_bookmark import FBookmark
    from signapp.models_bookmark import BBookmark
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
    franks = []
    branks = []
    
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

            bimage = list(BoardImage.objects.filter(
                Q(bno__exact = col)
            ))[0]

            bcollarbors.append((collarbor, bimage))
    else:
        fblist = FBookmark.objects.values('FNO')
        # print(fblist)
        bblist = BBookmark.objects.values('bNO')
        # print(bblist)

        counts = {}

        for fno in fblist:
            if fno['FNO'] in franks:
                counts[fno['FNO']] += 1
            else:
                counts[fno['FNO']] = 1
        
        counts = sorted(counts.items(), reverse=True, key=lambda x:x[1])[:5]

        for fno in counts:
            frank_list = Product.objects.all().get(
                Q(prdlstReportNo__exact = fno[0])
            )
            franks.append(frank_list)

        counts = {}

        for bno in bblist:
            if bno['bNO'] in branks:
                counts[bno['bNO']] += 1
            else:
                counts[bno['bNO']] = 1

        counts = sorted(counts.items(), reverse=True, key=lambda x:x[1])[:5]

        for bno in counts:
            brank_list = Board.objects.all().get(
                Q(bno__exact = bno[0])
            )

            bimage = list(BoardImage.objects.filter(
                Q(bno__exact = bno[0])
            ))[0]

            branks.append((brank_list, bimage))

    # print(fcollarbors)
    # print(bcollarbors)
    # print(branks)

    return render(request, 'mainapp/home.html', {'fcollarbors':fcollarbors[:3], 'bcollarbors':bcollarbors[:3], 'franks':franks[:3], 'branks':branks[:3]})