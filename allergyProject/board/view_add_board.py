from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Board
from signapp.models_bookmark import BBookmark
from datetime import date

@require_POST
def like_button_view(request):
    # POST 요청에서 필요한 데이터를 가져옵니다.
    get_bno = request.POST.get('bno')
    customer = request.user

    board = Board.objects.get(bno=get_bno)
    title = board.title

    # 현재 사용자와 제품에 대한 북마크가 이미 존재하는지 확인합니다.
    existing_bookmark = BBookmark.objects.filter(CNO=customer, bNO=board).first()

    if existing_bookmark:
        # 북마크가 이미 존재하는 경우, 북마크를 삭제하여 해제합니다.
        existing_bookmark.delete()
        return JsonResponse({'message': '북마크가 성공적으로 해제되었습니다.'})
    else:
        # 새로운 북마크를 생성합니다.
        bookmark = BBookmark.objects.create(
            TITLE=title,
            bNO=board,
            CNO=customer,
            CDATE=date.today()
        )
        return JsonResponse({'message': '북마크가 성공적으로 추가되었습니다.'})