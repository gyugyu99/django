import json
from pathlib import Path

# 1. 경로 설정
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. 환경변수 (비밀 설정 파일) 불러오기
with open(BASE_DIR / '.secret_config' / 'secret.json') as f:
    config_secret_str = f.read()

SECRET = json.loads(config_secret_str)

# 3. 보안 및 디버그 설정
# 기존의 고정된 문자열 대신 SECRET 객체에서 가져옵니다.
SECRET_KEY = SECRET.get('DJANGO_SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = []



# INSTALLED_APPS를 성격에 따라 분리-> 가독성을 높임
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

CUSTOM_APPS = [
    'todo',
    'users',
]

# 새로운 라이브러리(에디터, 이미지 정리, 쉘 확장)를 추가
THIRD_PARTY_APPS = [
    'django_extensions',
    'django_summernote', # 리치 텍스트 에디터 사용을 위함
    'django_cleanup',    # 데이터 삭제 시 실제 이미지 파일도 자동 삭제
]

INSTALLED_APPS = DJANGO_APPS + CUSTOM_APPS + THIRD_PARTY_APPS

# [필수 복구] 관리자 페이지와 세션 유지를 위한 미들웨어 설정
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# [필수 복구] 템플릿 엔진 설정 (admin 앱 사용을 위해 필요)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'ko-kr' # 한국어 설정
TIME_ZONE = 'Asia/Seoul' # 한국 시간 설정
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_DIRS = BASE_DIR / 'static'
STATICFILES_DIRS = [
    STATIC_DIRS,
]
STATIC_ROOT = BASE_DIR / '.static_root'


# ImageField를 사용하기 위한 미디어 파일 경로 설정을 추가
# MEDIA_URL: 웹브라우저에서 접근할 때 사용하는 URL 경로
MEDIA_URL = 'media/'
# MEDIA_ROOT: 실제 서버 컴퓨터에 파일이 저장되는 물리적 경로
MEDIA_ROOT = BASE_DIR / 'media'


# Summernote 에디터의 외관과 기능을 정의하는 상세 설정을 추가
SUMMERNOTE_CONFIG = {
    'iframe': True, # 보안을 위해 에디터를 별도의 프레임으로 분리

    'summernote': {
        'airMode': False, # 툴바를 숨기지 않고 항상 표시
        'width': '100%',
        'height': '480',
        'toolbar': [ # 사용자가 사용할 버튼들 정의 (글꼴, 색상, 사진 삽입 등)
            ['style', ['style']],
            ['font', ['bold', 'underline', 'clear']],
            ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['table', ['table']],
            ['insert', ['link', 'picture']],
            ['view', ['fullscreen']],
        ],
        'lang': 'ko-KR', # 에디터 UI 언어를 한국어로 설정
    },
    'attachment_require_authentication': True, # 로그인한 사용자만 파일 업로드 가능하게 설정
}


# login / logout
LOGIN_REDIRECT_URL = '/cbv/todo/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# auth 커스텀 유저 모델 선언해줘서 추가함 user/models.py
AUTH_USER_MODEL = 'users.User'


# email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = SECRET['EMAIL']['USER']
EMAIL_HOST_PASSWORD = SECRET['EMAIL']['PASSWORD']
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER