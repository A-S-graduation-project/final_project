from django.shortcuts import render
from .models_bookmark import FBookmark
from .models_bookmark import BBookmark

def bookmarks(request):
    # 현재 로그인한 사용자의 CNO 가져오기
    user = request.user  # 이 부분은 사용자 인증 시스템에 따라 다를 수 있습니다.

    # 해당 사용자의 북마크 가져오기
    fbookmarks = FBookmark.objects.filter(CNO=user)
    bbookmarks = BBookmark.objects.filter(CNO=user)

    context = {
        'product_bookmarks': fbookmarks,
        'board_bookmarks': bbookmarks,
    }

    return render(request, 'signapp/bookmark.html', context)