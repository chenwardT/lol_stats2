# -*- coding: utf-8 -*-
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

INTERNAL_IPS = ['192.168.1.4', '192.168.1.7']

INSTALLED_APPS += ('django_extensions',
                   'debug_toolbar',)