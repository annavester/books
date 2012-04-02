import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
DEBUG = False
TEMPLATE_DEBUG = DEBUG
PROJECT_DIR = os.path.dirname(__file__)
ADMINS = (
          ('Anna Vester', 'veannaa@gmail.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'django.db.backends.mysql'
DATABASE_HOST = '127.0.0.1'

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'static')
UPLOAD_DIR = os.path.join(MEDIA_ROOT, 'book_thumbs')
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/media/'
SECRET_KEY = '8dzc7j2^q$^(i2=x1r658oj!odfwrrt5wds&snbcyyg&8t8@&q'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS += (
     'django.core.context_processors.request',
)

ROOT_URLCONF = 'books_app.urls'
LOGIN_URL = '/login/'
TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, "templates"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    #'django.contrib.admindocs',    
    'books_app.accounts',
    'books_app.books',
    'books_app.authors',
    'books_app.readinglists',
    'endless_pagination',
)

try:
    from local_settings import *
except ImportError:
    pass
