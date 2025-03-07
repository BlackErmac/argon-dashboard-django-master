# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this

urlpatterns = [
    path('admin/', admin.site.urls),                # Django admin route
    path("", include("apps.authentication.urls", namespace='authentication')),  # Auth routes - login / register
    path("dashboard/", include("apps.home.urls" , namespace='home')),            # UI Kits Html files
    path("transportation/" , include("apps.transportation.urls" , namespace='transportation')),           # cars application
    path("maps/" , include("apps.maps.urls" , namespace='map')), # maps application

]
