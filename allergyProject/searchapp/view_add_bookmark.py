from django.http import HttpResponse
from searchapp.models import Product
from signapp.models_bookmark import FBookmark
from datetime import date

def like_button_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        fno = request.POST.get('fno')
        customer = request.user

        # Product 모델에서 prdlstReportNo와 일치하는 제품을 가져옵니다.
        try:
            product = Product.objects.get(prdlstReportNo=fno)
        except Product.DoesNotExist:
            return HttpResponse(f'<script>openModal("{message}")</script>')

        # 이미 해당 제품에 대한 즐겨찾기가 있는지 확인합니다.
        existing_bookmark = FBookmark.objects.filter(CNO=customer, FNO=product).first()

        if existing_bookmark:
            # 이미 저장된 즐겨찾기가 있으면 모달 창을 열어서 메시지를 표시합니다.
            message = 'Bookmark already exists'
            return HttpResponse(f'<script>openModal("{message}")</script>')
        else:
            # Bookmark 모델에 제품과 현재 로그인한 사용자를 연결하여 저장합니다.
            bookmark = FBookmark.objects.create(
                TITLE=title,
                FNO=product,
                CNO=customer,  # 현재 로그인한 사용자를 CNO 필드에 저장합니다.
                CDATE=date.today()
            )

            # 성공 메시지를 모달 창을 열어서 표시합니다.
            message = 'Success'
            return HttpResponse(f'<script>openModal("{message}")</script>')
    else:
        return HttpResponse('<script>alert("Invalid Request")</script>')