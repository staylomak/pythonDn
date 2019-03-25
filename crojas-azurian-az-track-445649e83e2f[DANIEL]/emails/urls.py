# -*- coding: utf-8 -*-


from django.conf.urls import url


from .views import SendDelayedEmails


urlpatterns = [
    url(r'enviar-pendientes/(?P<rut_empresa>[\S]+)/$', SendDelayedEmails.as_view()),
]
