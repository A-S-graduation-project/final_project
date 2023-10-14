from django.shortcuts import render
from board.models import Board
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse

def my_board(request):
    # 현재 로그인한 사용자의 cno 값을 가져옵니다.
    customer_cno = request.user.cno

    # 사용자가 작성한 글을 가져옵니다.
    customer_board = Board.objects.filter(cno=customer_cno)

    return render(request, 'signapp/myboard.html', {'customer_board': customer_board})

#게시글  삭제
@csrf_protect
def delete_board(request):
    get_bno = request.POST.get('bno')

    # 북마크 삭제
    Board.objects.filter(bno=get_bno).delete()

    # JSON 응답 반환
    data = {'message': '삭제되었습니다.'}
    return JsonResponse(data)