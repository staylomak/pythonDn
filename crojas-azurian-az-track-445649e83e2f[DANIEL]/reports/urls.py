# -*- coding: utf-8 -*-


from django.conf.urls import url


from .views import DynamicReportTemplateView
from .views import FailureReportTemplateView
from .views import GeneralReportTemplateView
from .views import ReporteConsolidadoTemplateView
from .views import SendedReportTemplateView


urlpatterns = [
    # urls para generar reportes
    url(r'^general/(?P<date_from>\d+)/(?P<date_to>\d+)/'
        '(?P<empresa>[\S]+)/(?P<tipo_receptor>[\w.%+-]+)/$',
        GeneralReportTemplateView.as_view()),
    url(r'^sended/(?P<date_from>\d+)/(?P<date_to>\d+)/'
        '(?P<empresa>[\S]+)/(?P<tipo_receptor>[\w.%+-]+)/$',
        SendedReportTemplateView.as_view()),
    url(r'^failure/(?P<date_from>\d+)/(?P<date_to>\d+)/'
        '(?P<empresa>[\S]+)/(?P<tipo_receptor>[\w.%+-]+)/$',
        FailureReportTemplateView.as_view()),

    # url reporte dinamico
    url(r'^export/(?P<date_from>\d+)/(?P<date_to>\d+)/'
        + '(?P<empresa>[\S]+)/(?P<correo>[\S]+)/(?P<folio>[\S]+)/'
        + '(?P<rut>[\S]+)/(?P<mount_from>[\S]+)/(?P<mount_to>[\S]+)/'
        + '(?P<fallidos>[\S]+)/(?P<op1>[\S]+)/(?P<op2>[\S]+)/(?P<op3>[\S]+)/$',
        DynamicReportTemplateView.as_view()),

    # reportes privados para consolidados solo de forma local
    url(r'^consolidados/', ReporteConsolidadoTemplateView.as_view()),
]
