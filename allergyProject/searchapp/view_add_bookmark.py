from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Product
from signapp.models_bookmark import FBookmark
from datetime import date

@require_POST
def like_button_view(request):
    # POST 요청에서 필요한 데이터를 가져옵니다.
    title = request.POST.get('title')
    fno = request.POST.get('fno')
    customer = request.user
    redirect_url = reverse('searchapp:Detail') + f'?pk={fno}'

    try:
        # 제품을 데이터베이스에서 찾습니다.
        product = Product.objects.get(prdlstReportNo=fno)
    except Product.DoesNotExist:
        messages.error(request, '제품을 찾을 수 없습니다.')
        return HttpResponseRedirect(redirect_url)  # 현재 페이지를 다시 렌더링

    # 현재 사용자와 제품에 대한 북마크가 이미 존재하는지 확인합니다.
    existing_bookmark = FBookmark.objects.filter(CNO=customer, FNO=product).first()

    if existing_bookmark:
        # 북마크가 이미 존재하는 경우, 북마크를 삭제하여 해제합니다.
        existing_bookmark.delete()
        messages.success(request, '북마크가 성공적으로 해제되었습니다.')
    else:
        # 새로운 북마크를 생성합니다.
        bookmark = FBookmark.objects.create(
            TITLE=title,
            FNO=product,
            CNO=customer,
            CDATE=date.today()
        )
        messages.success(request, '북마크가 성공적으로 추가되었습니다.')
    # 현재 페이지를 다시 렌더링
    
    return HttpResponseRedirect(redirect_url)