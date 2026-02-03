#forms.py를 따로 만드는 이유
# 유효성 검사 / HTML 생성에 용이 / 보안
from django_summernote.widgets import SummernoteWidget
from django import forms
from .models import Todo, Comment

# 1. Todo 생성시 사용하는 폼
class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        # forms.ModelForm 덕분에 이렇게만 지정해도 Todo모델 설계도를 전부 훑어봄
        fields = ['title', 'description', 'start_date', 'end_date']
        widgets = {
            'description': SummernoteWidget(),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '제목을 입력해주세요.'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }

# 2. Todo 수정 시 사용하는 폼 (완료 여부 추가)
class TodoUpdateForm(forms.ModelForm):
    # django의 forms.ModelForm 기능 그대로 물려받음
    class Meta:
    #메타데이터 설정
        model = Todo
        # 이 폼은 Todo 모델과 연결
        fields = ['title', 'description', 'start_date', 'end_date', 'is_completed', 'completed_image']
        widgets = {
            'description': SummernoteWidget(),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '제목을 입력해주세요.'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'completed_image': forms.FileInput(attrs={'class': 'form-control'})
        }
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message',]
        # label은 화면에 보에는 글자
        labels = {
            'message': '내용',
        }
        # widget은 실제 입력창의 종류
        widgets = {
            'message': forms.Textarea(attrs={    # attrs = Attributes(속성)
                'rows': 5, 'cols': 45, 'class': 'form-control', 'placeholder': '댓글 내용을 입력해'
            }),
        }

