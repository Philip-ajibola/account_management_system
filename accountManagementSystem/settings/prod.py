import os

from .general import *

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False

ALLOWED_HOSTS = []

DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'account_management_system_db',
        'USER': 'root',
        'PASSWORD': 'Bobbyjay1@2&3',
        'HOST': 'localhost',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_HOST_PASSWORD= os.environ['EMAIL_HOST_USER']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_PORT = os.environ['EMAIL_PORT']
DEFAULT_FROM_EMAIL = os.environ['DEFAULT_FROM_EMAIL']