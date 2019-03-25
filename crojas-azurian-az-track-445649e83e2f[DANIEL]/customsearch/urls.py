# -*- coding: utf-8 -*-


from django.conf.urls import url


from .views import IndexTemplateView
from .views import EmailDetailView
from .views import DynamicQueryView


urlpatterns = [
    # estas son las urls para las consultas que llenan la tabla html
    url(r'^$', IndexTemplateView.as_view(), name='index'),

    # consultas para el modal de detalle (cuando clickean un row de la tabla html)
    url(r'^email-detail/', EmailDetailView.as_view()),

    # consultas dinamicas
    url(r'^search/(?P<date_from>\d+)/(?P<date_to>\d+)/'
        + '(?P<empresa>[\S]+)/(?P<correo>[\S]+)/(?P<folio>[\S]+)/'
        + '(?P<rut>[\S]+)/(?P<mount_from>[\S]+)/(?P<mount_to>[\S]+)/'
        + '(?P<fallidos>[\S]+)/(?P<op1>[\S]+)/(?P<op2>[\S]+)/(?P<op3>[\S]+)/$',
        DynamicQueryView.as_view()),
]
