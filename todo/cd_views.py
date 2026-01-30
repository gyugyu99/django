from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from todo.models import Todo


class TodoListView(ListView):
    # CBV상속 (데이터 리스트 보여주기)
    queryset = Todo.objects.all()
    # todo/models.py의 Todo를 전부 가져와 쿼리셋에 할당
    paginate_by = 10
    # 페이지당 10개씩
    ordering =  ['-created_at', '-id']
    # 최신순 정렬
    template_name = 'todo/todo_list.html'

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        # super()로 클래스 부모의 쿼리셋 사용 / 로그인한 유저의 데이터만 가져옴
        if self.request.user.is_superuser:
            # 로그인한 유저가 super유저인지 확인하는 조건문
            queryset = super().get_queryset()
            # 부모 클래스의 쿼리셋 (모든 정보를 가져옴)

        q = self.request.GET.get('q')
        # URL 파라미터로 q라는 검색어가 전달되었을 경우
        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
            # 제목이나 내용에 q가 포함되어있다면
        return queryset
        # 쿼리셋을 리턴함

class TodoDetailView(LoginRequiredMixin, DetailView):
     # CBV상속 (데이터 상세정보 보기) LoginRequiredMixin = 로그인 확인
    model = Todo
    template_name = 'todo/todo_info.html'

    def get_object(self, queryset=None):
        # 상세페이지에서 DB 데이터중 1개만 들고올때
        obj = super().get_object(queryset)
             # 부모클래스의 'get_object'기능을 빌려와 Todo 데이터 한 덩이를 obj에 할당


        if obj.user != self.request.user and not self.request.user.is_superuser:
            # 방금 가져온 Todo 데이터의 주인과 현재 접속자가 다르거나, 관리자가 아니면? -> 에러발생
            raise Http404("해당 To Do를 조회할 권한이 없습니다.")
        return obj

    def get_context_data(self, **kwargs):
        # HTML로 보낼 데이터를 받음 (kwargs: 몇개인지 모르는 키워드 인자들 다받음)
        context = {'todo': self.object.__dict__}
        # get_object가 찾아낸 데이터 객체를 딕셔너리로 변경
        return context


class TodoCreateView(LoginRequiredMixin, CreateView):
    # 새로운 데이터 생성 (CreateView상속)
    model = Todo
    fields = ['title', 'description', 'start_date', 'end_date']
    template_name = 'todo/todo_create.html'

    def form_valid(self, form):
        # 유효성 검사
        self.object = form.save(commit=False)
        # DB에는 아직 안들어감 임시저장
        self.object.user = self.request.user
        # 요청한 유저 정보 -> user필드에 강제로 할당
        # 사용자가 입력하는 fields 목록에는 user가 없기 때문
        self.object.save()
        # DB에 최종 저장
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        # 글을 다 쓴 후 쓴 글의 상세 페이지로 이동
        return reverse_lazy('cbv_todo_info', kwargs={'pk': self.object.id})
        # reverse_lazy -> URL 이름을 실제 주소로 바꿔줌


class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    fields = ['title', 'description', 'start_date', 'end_date', 'is_completed', 'id']
    template_name = 'todo/todo_update.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404("해당 To Do를 수정할 권한이 없습니다.")
        return obj

    def get_success_url(self):
        return reverse_lazy('cbv_todo_info', kwargs={'pk': self.object.id})


class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404("해당 To Do를 삭제할 권한이 없습니다.")
        return obj

    def get_success_url(self):
        return reverse_lazy('cbv_todo_list')
