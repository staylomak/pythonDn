# -*- coding: utf-8 -*-


import json
import logging


from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView


from autenticacion.views import LoginRequiredMixin
from perfiles.models import Perfil
from utils.generics import timestamp_to_date
from webhooks.models import EmailLogEvent


logger = logging.getLogger(__name__)


class ResumenIndexView(LoginRequiredMixin, TemplateView):
    template_name = "resumen/index.html"

    def get(self, request, *args, **kwargs):
        perfil = Perfil.get_perfil(request.user)
        logger.info(perfil.usuario)
        data = {
            'empresas': perfil.empresas.all(),
        }
        return render(request, self.template_name, data)


class QueryTemplateView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):

        params = dict()

        date_from = request.GET['date_from']
        date_to = request.GET['date_to']
        params['empresa'] = request.GET['empresa']

        date_from = int(date_from, base=10)
        date_to = int(date_to, base=10)
        params['date_from'] = timestamp_to_date(date_from)
        params['date_to'] = timestamp_to_date(date_to)

        count = EmailLogEvent.get_count_by_months(**params)

        data = {
            'total': count,
        }
        return HttpResponse(json.dumps(data))
