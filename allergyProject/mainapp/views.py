from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.db.models import Q, Count

from searchapp.models import Product, Allergy
from board.models import Board, BoardImage
from signapp.models import Customer

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


def CheckAll(user):
    allergies = []

    user_allerinfo = Customer.objects.get(
        username = user.username
    ).allerinfo
    allerinfo_list = [int(item) for item in user_allerinfo.strip('[]').split(', ')]

    for ano in allerinfo_list:
        allergy = Allergy.objects.all().get(
            Q(ano__exact = ano)
        ).allergy
        allergies.append(allergy)

    aller_str = ', '.join(allergies)

    return aller_str


def Collarbor(request):
    username = request.user

    fcollarbors = []
    bcollarbors = []
    franks = []
    branks = []
    
    if not username.is_anonymous:
        allergies_str = CheckAll(username)
        fcollarbor_list = food_recommend(str(username)).keys()
        bcollarbor_list = board_recommend(str(username)).keys()

        for col in fcollarbor_list:
            collarbor = Product.objects.all().get(
                Q(prdlstReportNo__exact = col)
            )
            fcollarbors.append(collarbor)

        for col in bcollarbor_list:
            collarbor = Board.objects.all().get(
                Q(bno__exact=col)
            )
            bimage = BoardImage.objects.filter(bno=col).first()
            bcollarbors.append((collarbor, bimage))

        context = {
            'fcollarbors':fcollarbors[:3],
            'bcollarbors':bcollarbors[:3],
            'allergies_str':allergies_str,
        }

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
            bimage = BoardImage.objects.filter(bno=bno[0]).first()
            branks.append((brank_list, bimage))

        context = {
            'franks':franks[:3],
            'branks':branks[:3],
        }

    # print(fcollarbors)
    # print(bcollarbors)
    # print(branks)

    return render(request, 'mainapp/home.html', context)