import os

from .general import *

SECRET_KEY = os.environ['SECRET_KEY']


DEBUG = True

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
EMAIL_HOST = 'localhost'
EMAIL_HOST_PASSWORD= ''
EMAIL_HOST_USER = ''
EMAIL_PORT = 2525
DEFAULT_FROM_EMAIL = 'info@mjaizsbank.com'