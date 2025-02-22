from django.urls import path

from .views import (driver_create , driver_list , driver_update , driver_delete ,
                    car_create , car_list , car_update , car_delete, car_maintenance,
                    task_create , task_list , task_delete , task_update , task_finish)

app_name = 'transportation'

urlpatterns = [
    # Driver URLs
    path('drivers/', driver_list, name='driver_list'),
    path('driver/create/', driver_create, name='driver_create'),
    path('driver/<int:pk>/edit/', driver_update, name='driver_update'),
    path('driver/<int:pk>/delete/' , driver_delete , name = 'driver_delete'),
    # Car URLs
    path('cars/', car_list, name='car_list'),
    path('car/create/', car_create, name='car_create'),
    path('car/<int:pk>/edit/', car_update, name='car_update'),
    path('car/<int:pk>/delete/' , car_delete , name = 'car_delete'),
    path('car/<int:pk>/maintenance/' , car_maintenance , name = 'car_maintenance'),
    # Task URLs
    path('tasks/', task_list, name='task_list'),
    path('task/create/', task_create, name='task_create'),
    path('task/<int:pk>/edit/', task_update, name='task_update'),
    path('task/<int:pk>/delete/' , task_delete , name = 'task_delete'),
    path('task/<int:pk>/finish/' , task_finish , name = 'task_finish'),
    ]