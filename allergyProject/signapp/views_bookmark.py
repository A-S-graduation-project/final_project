from django.shortcuts import render
from .models_bookmark import FBookmark
from .models_bookmark import BBookmark

def bookmarks(request):
    # 현재 로그인한 사용자의 CNO 가져오기
    user = request.user  

    # 해당 사용자의 북마크 가져오기
    fbookmarks = FBookmark.objects.filter(CNO=user)
    bbookmarks = BBookmark.objects.filter(CNO=user)

    context = {
        'food_bookmarks': fbookmarks,
        'board_bookmark': bbookmarks,
    }

    return render(request, 'signapp/bookmark.html', context)