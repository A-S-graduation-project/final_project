from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView
from board.models import Board, Recipe
from .forms import BoardForm, RecipeForm


# Create your views here.
# def board (request):
#     return render(request, 'board.html')

class BoardView(ListView):
    model = Board
    queryset = Board.objects.order_by('bno')
    context_object_name = "board_list"

# def DetailView (request):
#     return render(request, 'boarddetail.html')

class DetailView(TemplateView):
    template_name = 'board/board_detail.html'


# class BoardCreateView(CreateView):
#     # template로 board_form.html을 가져와 사용
#     template_name = 'board/board_form.html'

#     # model은 Board form은 BoardForm을 사용
#     model = Board
#     form_class = BoardForm
    
#     # 성공시 돌아갈 URL로 board_list로 이동
#     success_url = reverse_lazy("board:board_list")

def create_board(request):
    if request.method == 'POST':
        board_form = BoardForm(request.POST, prefix='board')
        recipe_form = RecipeForm(request.POST, prefix='recipe')

        if board_form.is_valid() and recipe_form.is_valid():
            # 게시물 데이터 저장
            board = board_form.save()

            # 레시피 데이터 저장
            if recipe_form.cleaned_data.get('content'):
                recipe = recipe_form.save()
                board.recipes.add(recipe)

            return redirect('board_list')  # 적절한 리다이렉트 URL로 변경
    else:
        board_form = BoardForm(prefix='board')
        recipe_form = RecipeForm(prefix='recipe')

    return render(request, 'board_form.html', {'board_form': board_form, 'recipe_form': recipe_form})