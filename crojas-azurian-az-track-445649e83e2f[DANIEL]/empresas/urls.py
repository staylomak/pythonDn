# -*- coding: utf-8 -*-


from django.conf.urls import url

from .views import CamposOpcionalesEmailView

urlpatterns = [
    url(r'^optional-fields/(?P<empresa>\b\d{1,8}\-[K|0-9])/$',
        CamposOpcionalesEmailView.as_view(), name="campos"),
]
