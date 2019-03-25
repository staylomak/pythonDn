# -*- coding: utf-8 -*-


"""
Módulo de configuración de las tareas que puedan
ser creadas y ejecutadas en la aplicación.
(requiere de RabbitMQ-Server)
"""


from __future__ import absolute_import


import os


from django.conf import settings
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')


app = Celery('track')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
    broker_url='amqp://guest:guest@localhost//',
    beat_scheduler='django_celery_beat.schedulers.DatabaseScheduler',
)
