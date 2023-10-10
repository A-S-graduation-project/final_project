from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView
from board.models import Board, Comment, Image
from .forms import BoardForm, CommentForm, IngredientForm, ImageForm
from searchapp.models import Allergy
from django.utils import timezone
import datetime as dt
import json

class BoardView(ListView):
    model = Board
    queryset = Board.objects.order_by('bno')
    context_object_name = "board_list"

def read_board(request, bno):
    # 게시글을 데이터베이스에서 가져오거나 존재하지 않는 경우 404 에러 반환
    board = get_object_or_404(Board, bno=bno)
    # JSON 형식의 재료 데이터를 파이썬 객체로 변환
    ingredient_data = json.loads(board.ingredient)
    print(ingredient_data,'\n',board.ingredient)

    # 선택한 알러지 정보를 가져와서 알러지 객체와 매칭하여 이름만 가져옴
    selected_allergies = json.loads(board.allerinfo)
    allerinfo = [Allergy.objects.get(ano=allergy['ano']).allergy for allergy in selected_allergies]
    print(allerinfo)

    return render(request, 'board/board_detail.html', {'board': board, 'ingredient_data': ingredient_data, 'allerinfo':allerinfo})

# test 코드
def create_board(request):
    allergies = Allergy.objects.all()
    image_form = ImageForm(request.POST, request.FILES)

    if request.method == 'POST':
        print("----------- this method POST -----------")
        board_form = BoardForm(request.POST, request.FILES)
        ingredient_form = IngredientForm(request.POST, prefix='ingredient')  # IngredientForm
        print(f"{image_form} \n {request.FILES}")
        if 'images' in request.FILES:
            for uploaded_image in request.FILES.getlist('images'):
                image = Image.objects.create(image=uploaded_image)
                board.images.add(image)

        print(f"{board_form.is_valid()} and {ingredient_form.is_valid()} and {image_form.is_valid()}")
        if board_form.is_valid() and ingredient_form.is_valid():
            print("---------- valid form ----------")
            board = board_form.save(commit=False) # 데이터 베이스에 아직 저장하지 않고 board만 생성
            board.cdate = timezone.now()
            print(" ---------- save form and datetime -----------")
            if request.user.is_authenticated:
                board.name = request.user.username
                board.cno = 1
                # board.cno = request.user.cno
                print(" ---------- User -----------")
            else:
                print(" ---------- NO User -----------")

            selected_allergies = request.POST.getlist('selected_allergies')
            # 선택한 알러지 정보를 가져오고
            selected_allergies_objects = Allergy.objects.filter(ano__in=selected_allergies)
            # 선택한 알러지 정보를 Allergy 모델에서 가져옴

            # 게시판의 allerinfo 속성에 넣어준다.
            allergy_info = [{"ano": allergy.ano, "allergy": allergy.allergy} for allergy in selected_allergies_objects]
            board.allerinfo = json.dumps(allergy_info)
            
            print(f"\n--------{ingredient_form}--------\n-------------{request.POST.get('ingredient_name')}")

            # IngredientFormSet에서 필수 재료 데이터를 가져와서 JSON 형태로 변환하여 board의 ingredient에 설정
            ingredient_name = ingredient_form.cleaned_data.get('ingredient_name')
            quantity = float(ingredient_form.cleaned_data.get('quantity'))
            unit = ingredient_form.cleaned_data.get('unit')
            ingredients = {
                'ingredient_name': ingredient_name,
                'quantity': quantity,
                'unit': unit
            }
            print(f"\n--------{ingredients}--------\n")

            board.ingredient = json.dumps(ingredients)

            print(f"\n--------{board.ingredient}--------\n")
            
            if 'images' in request.FILES:
                for uploaded_image in request.FILES.getlist('images'):
                    image = Image.objects.create(image=uploaded_image)
                    board.images.add(image)
            
            # 모든 속성이 들어간 board를 저장해준다.
            board.save()
            print(f'{board} \n------------------')

            return redirect('../')
        
        print("----------- unvalid form -----------")
        print(f"{board_form.errors} {board_form.is_valid()} \n\n")
        print(f"{ingredient_form.errors} {ingredient_form.is_valid()}")
    else:
        print("---------- enter the create board page ----------")
        # method가 POST가 아니면 빈 form의 인스턴스를 생성한다.
        board_form = BoardForm()
        ingredient_form = IngredientForm(prefix='ingredient')  # 빈 IngredientFormSet 생성

    return render(request, 'board/board_form.html', {'board_form': board_form, 'ingredient_form' : ingredient_form, 'allergies': allergies, 'image_form': image_form})


def update_board(request, bno):
   # 수정할 게시글의 게시판 번호를 가져온다.
    board = get_object_or_404(Board, pk=bno)
    # 모든 알러지 정보를 가져온다.
    allergies = Allergy.objects.all()
    # form의 method가 POST로 오면
    if request.method == 'POST':
        # board의 form을 가져와 저장한다.
        board_form = BoardForm(request.POST)

        # board_form이 valid하다면
        if board_form.is_valid():
            # 데이터 베이스에 아직 저장하지 않고 board만 생성
            board = board_form.save(commit=False) 
            # udate의 경우 수정을 완료한 시간을 넣어준다.
            board.udate = dt.datetime.now()
            # 현재 작성하고 있는 사용자의 이름과 번호를 가져와 넣는다.
            board.name = request.user.username
            board.cno = request.user.cno

            # 사용자가 form에서 선택한 알러지 정보를 가져온다.
            selected_allergies = request.POST.getlist('selected_allergies')
            # 게시판의 allerinfo 선택 정보를 속성에 넣어준다.
            board.allerinfo = json.dumps(selected_allergies)
            # 모든 속성이 들어간 board를 저장해준다.
            board.save()
            
            # 성공하면 board_list로 이동한다.
            return redirect('board_list')
        
        # board_form unvalid하다면 error를 출력
        print(f"{board_form.errors}")
    else:
        # method가 POST가 아니면 bno에 해당하는 값을 form에 넣는다..
        board_form = BoardForm(instance=board)
    # board_form 페이지를 보여준다.
    return render(request, 'board/board_form.html', {'board_form': board_form, 'allergies': allergies})


def delete_board(request, bno):
    # 게시글을 삭제할 게시글 객체를 가져온다.
    board = get_object_or_404(Board, pk=bno)

    if request.method == 'POST':
        # 게시글을 삭제한다.
        board.delete()
        print("게시판이 삭제되었습니다.")
        return redirect('board_list')

def create_comment(request, bno):
    board = get_object_or_404(Board, pk=bno)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.bno = board
            comment.cdate = dt.datetime.now()
            comment.save()
            return redirect('board_detail', board_id=bno)
    else:
        comment_form = CommentForm()

    return render(request, 'board/board_detail.html', {'board': board, 'comment_form': comment_form})

def update_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    board_id = comment.bno.pk

    if request.method == 'POST':
        comment_form = CommentForm(request.POST, instance=comment)
        if comment_form.is_valid():
            # 댓글이 이미 존재하면 udate 업데이트
            if comment.cdate:
                comment.udate = dt.datetime.now()
            comment_form.save()
            return redirect('board_detail', board_id=board_id)



def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    board_id = comment.bno.pk

    if request.method == 'POST':
        comment.delete()
        return redirect('board_detail', board_id=board_id)