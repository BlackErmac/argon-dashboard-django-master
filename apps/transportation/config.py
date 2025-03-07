from django.apps import AppConfig
import threading
from .tasks import check_expired_tasks

class TransConfig(AppConfig):
    name = 'apps.transportation'
    label = 'apps_transportation'

    def ready(self):
        """Start the background task when Django starts."""
        threading.Thread(target=check_expired_tasks, daemon=True).start()