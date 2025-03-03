import time
from django.utils.timezone import now
from django.db import close_old_connections
from .models import Task, Notification

def check_expired_tasks():
    """Continuously check for expired tasks and create notifications."""
    while True:
        try:
            close_old_connections()  # Prevents database connection issues

            expired_tasks = Task.objects.filter(status='open')

            for task in expired_tasks:
                if now() >= (task.created_at + task.duration):
                    # Create a notification
                    Notification.objects.create(
                        task=task,
                        message=f"Task '{task.task_subject}' duration is over!",
                    )
                    # Mark task as completed
                    task.status = 'lated'
                    task.save()

        except Exception as e:
            print(f"Error in background task checker: {e}")

        time.sleep(60)  # Wait 60 seconds before checking again
