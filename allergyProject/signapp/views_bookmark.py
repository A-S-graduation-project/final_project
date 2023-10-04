from django.http import JsonResponse
from django.shortcuts import render
from .models_bookmark import FBookmark
from .models_bookmark import BBookmark
from django.views.decorators.csrf import csrf_protect

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

@csrf_protect
def delete_fbookmark(request):
    fmno = request.POST.get('fmno')

    # 북마크 삭제
    FBookmark.objects.filter(FMNO=fmno).delete()

    # JSON 응답 반환
    data = {'message': '찜 해제되었습니다.'}
    return JsonResponse(data)

@csrf_protect
def delete_bbookmark(request):
    bmno = request.POST.get('bmno')

    # 북마크 삭제
    BBookmark.objects.filter(BMNO=bmno).delete()

    # JSON 응답 반환
    data = {'message': '찜 해제되었습니다.'}
    return JsonResponse(data)