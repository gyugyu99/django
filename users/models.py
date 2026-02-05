# users/models.py

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class UserManger(BaseUserManager):
    def create_user(self, email, password, *args, **kwargs):
        #입력받은 파라미터로 유저 모델을 데이터베이스에 저장
        if not email:
            raise ValueError('Users must have an email address')
        #이메일 누락검사
        user = self.create(email=email, *args, **kwargs)
        #이메일 정규화
        user.set_password(password)
        #비밀번호 암호화
        user.save()
        return user

    def create_superuser(self, email, password, *args, **kwargs):
        user = self.create_user(email, password, *args, **kwargs)
        #create_user함수 사용
        user.is_staff = True
        #운영진 여부
        user.is_superuser = True
        #최고 권한
        user.is_active = True
        #활성 상태
        user.save(using=self._db)
        #데이터를 저장할 때 특정 데이터베이스에 저장하라고 지정하는 매개변수 옵션(현재 매니저가 관리하는 DB에 정확히 저장)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    #AbstractBaseUser = 완전 새 모델 구현을 위해 상속 (password와 last_login필드만 기본으로 제공)
    #PermissionsMixin = admin페이지나 기존 권한을 계속 사용하고 싶을 때 AbstractBaseUser와 함께 사용
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManger()
    #커스텀 유저 매니저

    USERNAME_FIELD = 'email'
    #email필드를 아이디로 (로그인시 ID)
    EMAIL_FIELD = 'email'
    #email필드를 email로 (비밀번호 찾기 메일 보냄)

    def __str__(self):
        return self.name

    @property
    #함수를 변수처럼 사용할 수 있게 해줌 ()안붙여도됨
    def username(self):
        return self.name