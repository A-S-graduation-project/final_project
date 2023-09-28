from django.shortcuts import render
from .models_bookmark import Bookmark

def bookmarks(request):
    # 현재 로그인한 사용자의 정보를 가져옵니다.
    current_user = request.user

    # 현재 사용자와 관련된 즐겨찾기 목록을 필터링합니다.
    user_bookmarks = Bookmark.objects.filter(CNO=current_user)

    return render(request, 'signapp/bookmark.html', {'bookmark': user_bookmarks})