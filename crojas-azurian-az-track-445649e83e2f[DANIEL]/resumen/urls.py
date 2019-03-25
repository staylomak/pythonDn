# -*- coding: utf-8 -*-


from django.conf.urls import url


from .views import ResumenIndexView
from .views import QueryTemplateView


urlpatterns = [
    url(r'^$', ResumenIndexView.as_view(), name="index"),
    url(r'^search/$', QueryTemplateView.as_view(), name="search"),
]
