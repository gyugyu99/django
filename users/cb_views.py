# users/cb_views.py

from django.contrib.auth import get_user_model, login
from django.core import signing
from django.core.signing import TimestampSigner, SignatureExpired
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, FormView
from users.forms import SignupForm, LoginForm
from django.shortcuts import render, get_object_or_404, redirect

from utils.email import send_email

User = get_user_model()


class SignupView(CreateView):
    # 회원가입(데이터 생성)기능을 가진 뷰
    template_name = "registration/signup.html"
    form_class = SignupForm
    # SignupForm을 지정함으로서 화면 구성, 데이터 검증, 데이터 저장 기능이 김

    def form_valid(self, form):
        #폼 데이터로 유저 모델을 저장할 때 인증 이메일을 보내는 기능
        user = form.save()
        #유저 모델 저장
        signer = TimestampSigner()
        #장고에서 제동하는 도장(서명)도구 -> 시간 정보를 함께 담는다
        signed_user_email = signer.sign(user.email)
        #유저의 이메일 뒤에 서명을 붙임
        signer_dump = signing.dumps(signed_user_email)
        #서명된 데이터를 URL에 안전하게 넣기 위해 문자열로 인코딩함(특수문자 등이 URL에서 깨지지 않게 압축)

        url = f"{self.request.scheme}://{self.request.META["HTTP_HOST"]}/users/verify/?code={signer_dump}"
        #실제 유저가 클릭할 주소 설정 scheme= http 또는 https
        subject = f"[Todo]{user.email}님의 이메일 인증 링크입니다."
        message = f"""
            아래의 링크를 클릭하여 이메일 인증을 완료해주세요.\n\n
            {url}
            """
        send_email(subject=subject, message=message, from_email=None, to_email=user.email)
        # utils.py에 만든 send_email 함수 사용

        return render(
            request=self.request,
            template_name="registration/signup_done.html",
            context={
                'user': user,
            }
        )


def verify_email(request):
    #이메일 검증 함수
    code = request.GET.get('code', '')
    # URL 쿼리 파라미터의 'code'부분 가져옴. 없다면? -> ''을 반환해라

    signer = TimestampSigner()
    #장고에서 제동하는 도장(서명)도구 -> 시간 정보를 함께 담는다
    try:
        decoded_user_email = signing.loads(code)
        # 해독된 유저 이메일 = URL을 타고온 code를 다시 파이썬이 읽을 수 있게 되돌림
        user_email = signer.unsign(decoded_user_email, max_age=60 * 5)
        # 유저 이메일 =. 도장을 검사하고 실제 알맹이를 꺼냄(max_age는 unsign최대시간 설정)
    except (TypeError, SignatureExpired):

        return render(request, 'registration/verify_failed.html')

    user = get_object_or_404(User, email=user_email)
    user.is_active = True
    user.save()
    return render(request, 'registration/verify_success.html')


class LoginView(FormView):
    #로그인 기능
    template_name = "registration/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("cbv_todo_list")

    def form_valid(self, form):
        user = form.get_user()
        #로그인 성공한 유저 객체를 안전하게 꺼내오는 통로
        login(self.request, user=user)
        return HttpResponseRedirect(self.get_success_url())