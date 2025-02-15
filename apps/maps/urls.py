from django.urls import path
from .views import show_map

app_name = 'maps'

urlpatterns = [
    path('' , show_map , name = 'show_map')
]