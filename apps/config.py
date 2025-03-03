from django.apps import AppConfig
import threading
from transportation.tasks import check_expired_tasks

class AppsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps'
    label = 'apps'

