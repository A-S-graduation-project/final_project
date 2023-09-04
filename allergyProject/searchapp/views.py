from django.shortcuts import render
from .models import Product
from .models import UserData
from django.db.models import Q
try:
    from searchapp.allergy_sim import *
    from searchapp.food_sim import *
except:
    pass

# filter 함수의 Q함수: OR조건으로 데이터를 조회하기 위해 사용하는 함수
# objects.filter() 는 특정 조건에 해당하면 객체 출력 .get('kw') 은 kw만 반환
# __icontains 연산자 : 대소문자를 구분하지 않고 단어가 포함되어 있는지 검사. 사용법 "필드명"__icontains = 조건값

def filtering(products, list, query):
    if list != []:
        for i in list:
            products = products.filter(
                    (Q(prdlstNm__icontains=query) |
                    Q(prdkind__icontains=query)) &
                    ~Q(allergy__icontains=i)
                )
            list.remove(i)
            return filtering(products, list, query)
    return products


def searchResult(request):
    # global query
    if ('kw' in request.GET) and ('afilter' in request.GET):
        query = request.GET.get('kw')
        afilter = request.GET.getlist('afilter')
        list = afilter.copy()
        products = Product.objects.all().order_by('prdlstNm')
        products = filtering(products, list, query)[:200]
        return render(request, 'search.html', {'query':query, 'afilter':afilter, 'products':products} )
    
    elif ('kw' in request.GET):
        query = request.GET.get('kw')
        products = Product.objects.all().order_by('prdlstNm')
        products = products.filter(
            Q(prdlstNm__icontains=query) |
            Q(prdkind__icontains=query)
        )[:200]
        return render(request, 'search.html', {'query':query, 'products':products} )


def Detail(request):
    if ('pk' in request.GET):
        pk = request.GET.get('pk')
        detail = Product.objects.all()
        detail = detail.get(
            Q(prdlstReportNo__exact=pk)
        )

    try:
        user=UserData.objects.all().filter(
            Q(prdlstReportNo__exact=pk)
        )
    except UserData.DoesNotExist:
        user=UserData()
        user.gender='남성'
        user.older=25
        user.allergy='난류'
        user.prdlstNm=detail.prdlstNm
        user.rating=3
        user.prdlstReportNo=detail.prdlstReportNo
        user.save()

    collarbors = []
    similarities = []

    for i in range(len(re)):
        if i == 5:
            break
        colquery = re[i][1]
        collarbor = Product.objects.all()
        collarbor = collarbor.get(
            Q(prdlstReportNo__exact=colquery)
        )
        collarbors.append(collarbor)

    if ('pk' in request.GET):
        pk = request.GET.get('pk')
        id = prdlstReportNo.index(pk)
        for j in range(len(food_simi_cate[id])):
            if food_simi_cate[id][j] >= 0.7 and id != j:
                simquery = prdlstReportNo[j]
                try:
                    int(simquery)
                except ValueError:
                    continue
                similarity = Product.objects.all()
                similarity = similarity.get(
                    Q(prdlstReportNo__exact = simquery)
                )
                similarities.append(similarity)

    try:
        return render(request, 'detail.html', {'pk':pk, 'detail':detail, 'collarbors':collarbors, 'similarities':similarities})
    except:
        return render(request, 'detail.html', {'pk':pk, 'detail':detail})
