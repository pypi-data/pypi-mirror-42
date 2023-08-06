#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '1'
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.humanize',
    'cms',
    'menus',
    'treebeard',

    'djcms_blog',

    'djcms_blog_plugin',
)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['', ],
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
CMS_LANGUAGES = {
    1: [{
        'code': 'en',
        'name': 'English',
    }]
}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
    }
}
LANGUAGE_CODE = 'en'

DJCMS_BLOG_ID = 1
DJCMS_BLOG_ENTRIES_NUMBER = 5
SITE_ID = 1
