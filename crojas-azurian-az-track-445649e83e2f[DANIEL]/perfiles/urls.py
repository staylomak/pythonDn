# -*- coding: utf-8 -*-


from django.conf.urls import url


from .views import PerfilesView


urlpatterns = [
    url(r'^$', PerfilesView.as_view(), name="index"),
]
