# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

app_name = 'home'

urlpatterns = [

    path('', views.index, name='index'),
    re_path(r'^.*\.*', views.pages, name='pages'),

]
