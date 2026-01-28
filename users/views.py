# users/views.py

from django.conf import settings
# 장고 설정 관련 모듈
from django.shortcuts import render, redirect
# HTML 템플릿 렌더링 응답, 다른 URL로 강제 이동
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# django.contrib.auth (장고가 기본 제공하는 인증 시스템) import 회원가입용 폼 클래스, 로그인용 폼클래스
from django.contrib.auth import login as django_login
#login 함수 이름 충돌 방지

#회원가입 뷰
def sign_up(request):
    #request는 브라우저에서 들어온 HTTP 요청 객체
    form = UserCreationForm(request.POST)
    # POST요청으로 넘어온 데이터를 회원가입용 폼에 담고, 그걸 form 변수에 담음
    if form.is_valid():
        # 장고 내장함수 / form 유효성 검사 실행 -> 통과하면 True 반환
         form.save()
        # 새 User객체가 DB에 저장됨 + 비번은 자동으로 해시처리 User.objects.create() 안써도돼
         return redirect(settings.LOGIN_URL)
        # 회원가입 성공 후 settings의 설정 URL로 이동

    context = {'form': form}
    #템플릿으로 넘길 데이터 { 템플릿에서 사용할 이름: 실제 폼 객체 }
    return render(request, 'registration/signup.html', context)
    # signup.html 템플릿 렌더링 / context 전달

#로그인 뷰
def login(request):
    # 장고의 login()과 이름이 겹치기 떄문에 alias 처리함
    form = AuthenticationForm(request, data=request.POST or None)
    # POST 요청이면 데이터 사용, GET 요청이면 None / ⭐️로그인폼은 반드시 request 객체 필요
    if form.is_valid():
        #유효성 검사
        django_login(request, form.get_user())
        # form.get_user() 인증된 객체 반환 / django_login 세션 생성, 로그인 상태 유지
        return redirect(settings.LOGIN_REDIRECT_URL)
        #로그인 후 이동 페이지
    context = {'form': form}
    return render(request, 'registration/login.html', context)
