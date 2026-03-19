# Source - https://stackoverflow.com/a/72569646
# Posted by Himanshu Poddar, modified by community. See post 'Timeline' for change history
# Retrieved 2026-03-19, License - CC BY-SA 4.0

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app
__all__ = ['celery_app']
