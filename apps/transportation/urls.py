from django.urls import path

from .views import (driver_create , driver_list , driver_update , driver_delete ,
                    car_create , car_list , car_update , car_delete, car_maintenance,
                    task_create , task_list , task_delete , task_update , task_finish , task_print,
                    notification_create , notification_list , notification_delete , notification_update,notification_detail,
                    get_objects,
                    map_view,save_route,routes_map)

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
    path('task/<int:pk>/print/' , task_print , name = 'task_print'),
    # Notifications URLs
    path('notification/' , notification_list , name = 'notification_list' ),
    path('notification/create/', notification_create, name='notification_create'),
    path('notification/<int:pk>/edit/', notification_update, name='notification_update'),
    path('notification/<int:pk>/delete/' , notification_delete , name = 'notification_delete'),
    path('notification/<int:pk>/detail/' , notification_detail , name = 'notification_detail'),
    path("get_objects/", get_objects, name="get_objects"),
    #maps
    path("map", map_view, name="map"),
    path("map/save_route/", save_route, name="map_save_route"),
    path("map/routes_map/", routes_map, name="map_routes"),
    ]