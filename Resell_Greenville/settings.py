from pathlib import Path
import os

# 📌 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 📌 安全设置
SECRET_KEY = 'django-insecure-94+9^m4cdoio$q7^)*&wm3r(g=ruy%il$^i4-*uu#wx_o0)i32'
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# 📌 应用列表
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'user',
    'merchandise',
    'message',
]

# 📌 认证系统
AUTHENTICATION_BACKENDS = [
    'user.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# 📌 中间件（跨域必须放最前面）
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # ✅ 允许跨域
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
CORS_ALLOW_ALL_ORIGINS = True
# 📌 允许跨域的来源（Vue 前端地址）
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",  # Vue 开发环境
    "http://127.0.0.1:8080",
    "http://localhost:5173",  # Vite 开发环境
    "http://127.0.0.1:5173",
]

# 📌 允许跨域携带 Cookie（必须）
CORS_ALLOW_CREDENTIALS = True

# 📌 允许跨域的请求头
CORS_ALLOW_HEADERS = [
    "authorization",
    "content-type",
]

# 📌 允许 Vue 访问 Django 的 CSRF 保护
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

CORS_ALLOW_HEADERS = [
    "authorization",
    "content-type",
    "x-csrftoken",  # 允许 X-CSRFToken 头
]
CSRF_TRUSTED_ORIGINS = ["http://localhost:8080"]  # 允许 Vue 访问 CSRF 受信任的 API
# 📌 Session 设置（跨域必须）
SESSION_ENGINE = "django.contrib.sessions.backends.db"  # 采用数据库存储Session
SESSION_COOKIE_SAMESITE = None  # ✅ 允许跨域Session
SESSION_COOKIE_SECURE = False  # ⚠️ 开发环境下必须 False，生产环境改 True
SESSION_COOKIE_HTTPONLY = False  # 测试时允许前端读取
SESSION_COOKIE_SAMESITE = None
# 📌 URL 配置
ROOT_URLCONF = 'Resell_Greenville.urls'

# 📌 模板配置
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

# 📌 WSGI 配置
WSGI_APPLICATION = 'Resell_Greenville.wsgi.application'

# 📌 数据库（SQLite，可改为PostgreSQL）
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 📌 密码验证
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 📌 语言与时区
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# 📌 媒体文件（用户上传的图片）
MEDIA_URL = '/media/'  # ✅ 访问上传文件的URL前缀
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # ✅ 上传文件存储路径

# 📌 静态文件
STATIC_URL = 'static/'

# 📌 默认主键字段
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 📌 电子邮件（Gmail SMTP）
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'zhengdongyaoo@gmail.com'
EMAIL_HOST_PASSWORD = 'pjwkzbqdtejavksx'
DEFAULT_FROM_EMAIL = 'zhengdongyaoo@gmail.com'

# 📌 自定义用户模型
AUTH_USER_MODEL = 'user.CustomUser'
