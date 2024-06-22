from .celery import app as celery_app 
from .templatetags import custom_tags

__all__ = ['celery_app',]
