from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, ListView
from board.models import Board, Comment, BoardImage, TypeCategories, MeterialCategories, BSimilarity
from .forms import BoardForm, CommentForm, ImageForm, CommentForm
from searchapp.models import Allergy
from signapp.models import Customer
from django.utils import timezone
import datetime as dt
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import json

from similarity import board_sim

def board_view(request):
    # board 유사도 구하기
    board_sim()
    board_list = Board.objects.order_by('bno')
    boards = []
    
    # images_for_board = BoardImage.objects.get(bno=board_list.bno).first()
    
    for board in board_list:
        images_for_board = BoardImage.objects.filter(bno=board.bno)
        # 보드에 이미지가 있는 경우, 첫 번째 이미지를 저장합니다.
        first_image = images_for_board.first() if images_for_board else None
        
        # 보드와 해당 보드의 첫 번째 이미지를 튜플로 묶어 리스트에 추가합니다.
        boards.append((board, first_image))

    return render(request, 'board/board_list.html', {'boards': boards})

def read_board(request, bno):
    # 게시글을 데이터베이스에서 가져오거나 존재하지 않는 경우 404 에러 반환
    board = get_object_or_404(Board, bno=bno)
    board_list = Board.objects.all().order_by('bno')
    # 게시글에 해당하는 image가져오기
    images = list(BoardImage.objects.filter(bno=board))
    comment_form = CommentForm()
    comments = Comment.objects.filter(bno=board)
    writen_comment = []
    for comment in comments:
        comment_user = Customer.objects.get(cno=comment.cno)
        writen_comment.append((comment,comment_user))

    # 유사한 board객체들을 불러오는 부분 유사도 0.7이상
    sim_board = BSimilarity.objects.get(bno=bno).simlist
    similarities = []
    print(f"sim_board = {sim_board}")
    for sim_no in sim_board:
            similarity = Board.objects.all()
            similarity = similarity.get(
                Q(bno__exact = sim_no)
            )
            sim_image = BoardImage.objects.filter(bno=sim_no).first()
            similarities.append((similarity, sim_image))

    # 선택한 알러지 정보를 가져와서 알러지 객체와 매칭하여 이름만 가져옴
    selected_allergies = board.allerinfo
    allerinfo = [allergy for allergy in selected_allergies]
    recipe_image = [img.image for img in images[1:] if img.image != None ]
    recipe_ex_image = [img.ex_image for img in images[1:]]
    # print(f"internal = {recipe_image}")
    # print(f"external = {recipe_ex_image}")
    # print(f"{recipe_image != None}")
    if recipe_image:
        recipes = list(zip(board.content, recipe_image))
    else:
        recipes = list(zip(board.content, recipe_ex_image))
    return render(request, 'board/board_detail.html', {
        'board_list': board_list,
        'board': board, 
        'allerinfo':allerinfo,
        'images':images[0],
        'comment_form':comment_form,
        'comments':comments,
        'writen_comment': writen_comment,
        'recipes':recipes,
        'sim_board':similarities[:5],
        })
# test 코드

def create_board(request):
    allergies = Allergy.objects.all()
    type_category = TypeCategories.objects.all()
    meterial_category = MeterialCategories.objects.all()
    image_form = ImageForm(request.POST, request.FILES)

    if request.method == 'POST':
        print("----------- this method POST -----------")
        board_form = BoardForm(request.POST, request.FILES)
        print("----------- board form -----------")
        print(board_form)
        if board_form.is_valid():
            print("---------------- valid form ----------------")
            board = save_board(request, board_form, image_form)

            return redirect('../')
        print("---------------- unvalid form ----------------")
        print(board_form.errors)
    else:
        board_form = BoardForm()

    return render(request, 'board/board_form.html', {
        'board_form': board_form, 
        'allergies': allergies, 
        'image_form': image_form,
        'type_category':type_category,
        'meterial_category':meterial_category,
        })

def save_board(request, board_form, image_form):
    board = board_form.save(commit=False)
    board.cdate = timezone.now()
    print(request.user.username,request.user.cno)
    if request.user.is_authenticated:
        board.name = request.user.username
        board.cno = request.user.cno
    else:
        board.cno = None

    selected_allergies = request.POST.getlist('selected_allergies')
    selected_allergies_objects = Allergy.objects.filter(ano__in=selected_allergies)
    allergy_info = [allergy.allergy for allergy in selected_allergies_objects]
    board.allerinfo = allergy_info
    print(board.allerinfo)

    # 사용자로부터 선택받은 카테고리 정보를 가져와서 게시판 객체에 설정
    print("category save하는곳")
    type_category_id = request.POST.get('type_category_id')
    meterial_category_id = request.POST.get('meterial_category_id')
    print(type_category_id,meterial_category_id)

    type_category = TypeCategories.objects.get(types=type_category_id)
    meterial_category = MeterialCategories.objects.get(meterials=meterial_category_id)

    board.types = type_category.types
    board.meterials = meterial_category.meterials
    print("------------ before ------------")
    board.save()
    print("---------------- save board ----------------")
    handle_uploaded_images(request, board, image_form)

    return board

def handle_uploaded_images(request, board, image_form):
    if 'image' in request.FILES:
        print("---------------- valid imageform ----------------")
        for uploaded_image in request.FILES.getlist('image'):
            image = BoardImage.objects.create(bno=board, image=uploaded_image)
            image.save()

def update_board(request, bno):
    # 수정할 기존 보드 인스턴스를 가져옵니다.
    print("----------update----------")
    board = get_object_or_404(Board, pk=bno)

    # 폼에 필요한 모든 데이터를 검색합니다.
    allergies = Allergy.objects.all()
    type_category = TypeCategories.objects.all()
    meterial_category = MeterialCategories.objects.all()
    image_form = ImageForm(request.POST, request.FILES)

    print(f"------{board.allerinfo}-------{board.types}------{board.meterials}------{image_form}---------")


    if request.method == 'POST':
        board_form = BoardForm(request.POST, request.FILES, instance=board)  # 기존 보드를 수정하기 위해 인스턴스 전달
        if board_form.is_valid():
            board = save_board(request, board_form, image_form)
            return redirect('../')  # 수정 후 적절한 페이지로 이동

    else:
        board_form = BoardForm(instance=board)  # 기존 보드 데이터로 폼을 채웁니다.
        print(board_form)
        

    return render(request, 'board/board_form.html', {
        'board_form': board_form,
        'allergies': allergies,
        'image_form': image_form,
        'type_category': type_category,
        'meterial_category': meterial_category,
    })


def delete_board(request, bno):
    # 게시글을 삭제할 게시글 객체를 가져온다.
    board = get_object_or_404(Board, pk=bno)

    if request.method == 'POST':
        # 게시글을 삭제한다.
        board.delete()
        print("게시판이 삭제되었습니다.")
        return redirect('../../')

def board_filtering(boards, list, query):
    if list != []:
        for i in list:
            boards = boards.filter(
                    (Q(title__icontains=query) |
                    Q(types__icontains=query)) &
                    ~Q(allerinfo__icontains=i)
                )
            list.remove(i)
            return board_filtering(boards, list, query)
    return boards



def board_search_result(request):
    # board 유사도 구하기
    board_sim()
    boards = []

    if ('kw' in request.GET):
        if ('afilter' in request.GET):
            query = request.GET.get('kw')
            afilter = request.GET.getlist('afilter')
            list = afilter.copy()
            board_list = Board.objects.all().order_by('bno')
            board_list = board_filtering(board_list, list, query)[:1000]

            for board in board_list:
                first_image = BoardImage.objects.filter(bno=board.bno).first()
                boards.append((board, first_image))

            return render(request, 'board/board_search.html', {'query':query, 'afilter':afilter, 'boards':boards} )
    
        else:
            query = request.GET.get('kw')
            board_list = Board.objects.all().order_by('bno')
            board_list = board_list.filter(
                Q(title__icontains=query) |
                Q(types__icontains=query)
            )[:1000]

            for board in board_list:
                first_image = BoardImage.objects.filter(bno=board.bno).first()
                boards.append((board, first_image))

            return render(request, 'board/board_search.html', {'query':query, 'boards':boards} )

    return render(request, 'board/board_search.html', {'boards':boards})


@login_required
def create_comment(request, bno):
    board = get_object_or_404(Board, pk=bno)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.bno = board
            comment.cno = request.user.cno
            comment.cdate = timezone.now()
            comment.save()
            print(comment)
    return redirect(reverse('board:board_detail', args=[bno]))
    
def update_comment(request, bno, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    board_id = comment.bno.pk

    if request.method == 'POST':
        comment_form = CommentForm(request.POST, instance=comment)
        if comment_form.is_valid():
            # 댓글이 이미 존재하면 udate 업데이트
            if comment.cdate:
                comment.udate = dt.datetime.now()
            comment_form.save()
            return redirect(reverse('board:board_detail', args=[board_id]))


def delete_comment(request, bno, serialno):
    comment = get_object_or_404(Comment, serialno=serialno)

    if request.method == 'POST':
        comment.delete()
        return redirect(reverse('board:board_detail', kwargs={'bno': bno}))