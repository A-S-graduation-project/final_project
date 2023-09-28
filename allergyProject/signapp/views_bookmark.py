from django.shortcuts import render
from .models_bookmark import Bookmark

def bookmarks(request):
    # 현재 로그인한 사용자의 CNO 가져오기
    user = request.user  # 이 부분은 사용자 인증 시스템에 따라 다를 수 있습니다.

    # 해당 사용자의 북마크 가져오기
    bookmarks = Bookmark.objects.filter(CNO=user)

    # Product와 Board 분리
    product_bookmarks = bookmarks.filter(FNO__isnull=False)
    board_bookmarks = bookmarks.filter(BNO__isnull=False)

    context = {
        'product_bookmarks': product_bookmarks,
        'board_bookmarks': board_bookmarks,
    }

    return render(request, 'signapp/bookmark.html', context)