from django.shortcuts import render
from board.models import Board

def my_board(request):
    # 현재 로그인한 사용자의 cno 값을 가져옵니다.
    user_cno = request.user.cno

    # 사용자가 작성한 글을 가져옵니다.
    user_posts = Board.objects.filter(cno=user_cno)

    return render(request, 'signapp/myboard.html', {'user_posts': user_posts})
