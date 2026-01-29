from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from todo.forms import TodoForm, TodoUpdateForm
from todo.models import Todo

# @login_required() 장고가 제공하는 로그인한 사람만 들어오도록 제한을 둠
@login_required()
def todo_list(request):
    todo_list = Todo.objects.filter(user=request.user).order_by('created_at')
    # 로그인한 사람(request.user) 데이터만 뽑기 위해 filter / 오래된 순 정렬
    q = request.GET.get('q')
    # GET은 request 안에 들어있는 주소창 데이터 전용 칸
    # request.GET (사용자가 보낸 URL 파라미터들이 담긴 주머니) / .get('q') 그 주머니중 1개

    if q:
        todo_list = todo_list.filter(Q(title__icontains=q) | Q(description__icontains=q))
        # filter()안에 Q(조건) | Q(조건)  😒제목에 q가 포함되어있거나, 😒내용에 q가 포함된 것을 필터링한다.
    paginator = Paginator(todo_list, 10)
    #페이지네이터 구현 10개씩 묶어서 한 페이지로 만듦
    page_number = request.GET.get('page')
    # 페이지 숫자는 URL 쿼리스트링의 page= 에서 가져옴
    page_obj = paginator.get_page(page_number)
    #페이지를 잘라줌
    context = {
        'page_obj': page_obj    # HTML로 보낼 데이터를 담음
    }
    print(page_obj)
    return render(request, 'todo/todo_list.html', context)


@login_required()
def todo_info(request, todo_id):
    # todo의 세부내용을 보여주는 함수
    todo = get_object_or_404(Todo, id=todo_id)
    # 해당 id를 가진 데이터를 가져오되, 없으면 에러 대신 404를 띄움
    context = {
        'todo': todo.__dict__  # todo를 딕셔너리로 변환. HTML에서 반복문 .items를 쓰기 위해
    }
    return render(request, 'todo/todo_info.html', context)


@login_required()
def todo_create(request):
    # 할 일 생성
    form = TodoForm(request.POST or None)
    # 사용자가 데이터를 쓰고 '제출'을 누르면 request.POST가 데이터를 담고 첫 페이지면 None반환
    # forms.py에서 form데이터를 넘겨받음
    if form.is_valid():
        # is_valid() 검사값이 True면
        todo = form.save(commit=False) # ⭐️
        # DB에 바로 저장하지않고 잠깐 멈춤 (누구의 글인지user를 적지 않았기 때문)->form에는 user기입칸이 없음
        todo.user = request.user
        # 유저 칸에 현재 로그인한 사용자 정보 추가
        todo.save()
        # 완벽하니 DB에 저장함.
        return redirect(reverse('todo_info', kwargs={'todo_id': todo.pk}))
    context = {    # reverse 덕분애 todo_info -> todo/<int:todo_id>/가 됨, todo.pk는 장고 약속(이 데이터의 고유번호를 장고가 가져다줌)
        'form': form
    }
    return render(request, 'todo/todo_create.html', context)


@login_required()
def todo_update(request, todo_id):
    # 내용 수정
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    # 수정할 데이터를 가져오는데 user=request.user -> 남의 글은 수정 못함
    form = TodoUpdateForm(request.POST or None, instance=todo)
    # form.py에서 받아옴, instance=todo: 빈 폼이 아니라 아까 가져온 todo 데이터가 미리 채워진 폼을 보여줌
    if form.is_valid():
        form.save()
        return redirect(reverse('todo_info', kwargs={'todo_id': todo.pk}))
    context = {
        'form': form
    }
    return render(request, 'todo/todo_update.html', context)


@login_required()
def todo_delete(request, todo_id):
    #데이터를 지우는 로직
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    todo.delete()
    return redirect(reverse('todo_list'))