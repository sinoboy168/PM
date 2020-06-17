"""
Django settings for opms project.

*   为可选修改项目
**  为必须修改的项目

"""

import os, sys

######################################
# 配置相关目录
######################################
#当前目录往上两层路径，及项目的路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 自建APP
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# 第三方APP
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))


######################################
# 安全配置
######################################
SECRET_KEY = '2=x8z8e4psmp17sgdd@cripned2kj#jbuyz-wpam=c^p0$i^ew'

DEBUG = True#代码修改后，自动重新加载，html代码修改除外

ALLOWED_HOSTS = ['*']


######################################
# 缓存默认设置：本地的内存
######################################
{
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'global-variables'
    }
}
######################################
# 定义 APP
######################################
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # users
    'users',
    # 分页
    'pure_pagination',

    # 资产管理
    'asset_management',

    # 平台管理
    'platform_management',
    # 消息
    'message',
    # 文档
    'document_management',

    #操作记录
    'operation_record',

    #自动增加任务
    'django_apscheduler',

    #任务池
    'task_pool',

    # captcha
    'captcha',
]


######################################
# 中间件配置
######################################
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'login_check.UserLoginMiddleware'#zrz4/14新增  登录状态检测
]

ROOT_URLCONF = 'opms.urls'


######################################
# 模板配置
######################################
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Media 配置
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'opms.wsgi.application'


######################################
# ** 数据库配置
######################################


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', #固定配置
        'HOST': '127.0.0.1',#mysql地址
        'PORT': '3306',#端口号
        'NAME': 'opms',#库名（组名）
        'USER': 'root',#用户
        'PASSWORD': 'yourpassword',#密码
        'OPTIONS': {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                    "init_command": "SET foreign_key_checks = 0;",},
    }
}




######################################
# 认证配置
######################################
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# 定义认证模型
AUTH_USER_MODEL = 'users.UserProfile'


# 邮箱登陆
AUTHENTICATION_BACKENDS = (
    'users.views.OtherLoginBackend',
)


LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


######################################
# 静态文件配置
######################################
STATIC_URL = '/static/'

# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


######################################
# 上传文件配置
######################################
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


######################################
# ** 系统发件箱
######################################
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = False
# 所用邮箱的smtp地址
EMAIL_HOST = ''
EMAIL_PORT = 25
# 邮箱地址
EMAIL_HOST_USER = ''
# 邮箱密码
EMAIL_HOST_PASSWORD = ''
# 发件箱名字，和邮箱地址一样就行了
DEFAULT_FROM_EMAIL = ''


######################################
# 分页规则
######################################
PAGINATION_SETTINGS = {
    # 中间部分显示的页码数
    'PAGE_RANGE_DISPLAYED': 5,
    # 前后页码数
    'MARGIN_PAGES_DISPLAYED': 2,
    # 是否显示第一页
    'SHOW_FIRST_PAGE_WHEN_INVALID': False,
}


######################################
# ** 系统地址
######################################
SERVER_URL = 'http://192.168.10.100:8000'

# 远程服务部署的主机和端口
WEBSSH_IP = '192.168.10.100'
WEBSSH_PORT = '10001'

# 高德地图 API
GAODE_API_KEY = ''

# 默认城市编码，如深圳：440300
CITY_ID = '440300'

# 开发者邮箱
DEVELPER_EMAIL_ADDRESS = ''

# session 设置
# 30分钟
SESSION_ENGINE = 'django.contrib.sessions.backends.db'   # 引擎（默认）
SESSION_COOKIE_AGE = 6000 * 30#
SESSION_SAVE_EVERY_REQUEST = True
# 关闭浏览器，则COOKIE失效
SESSION_EXPIRE_AT_BROWSER_CLOSE = True



