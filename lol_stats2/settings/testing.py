# -*- coding: utf-8 -*-
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

# Using env var CELERY_ALWAYS_EAGER during testing. If we need everything/more of what
# CeleryTestRunner enables then install djcelery and uncomment the following:
# TEST_RUNNER = 'djcelery.contrib.test_runner.CeleryTestSuiteRunner'