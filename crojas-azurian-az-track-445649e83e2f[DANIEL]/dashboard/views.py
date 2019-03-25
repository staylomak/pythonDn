# -*- coding: utf-8 -*-


import json
import logging


from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView


from autenticacion.views import LoginRequiredMixin
from emails.models import Email
from perfiles.models import Perfil
from utils.generics import timestamp_to_date


logger = logging.getLogger(__name__)


class StatisticsView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        try:
            date_from = request.GET['date_from']
            date_to = request.GET['date_to']
            date_from = int(date_from, base=10)
            date_to = int(date_to, base=10)

            query_params = dict()
            query_params['date_from'] = timestamp_to_date(date_from)
            query_params['date_to'] = timestamp_to_date(date_to)
            query_params['empresa'] = request.GET['empresas']
            query_params['tipo_receptor'] = request.GET['tipo_receptor']

            statistic = Email.get_statistics_count_by_dates(**query_params)
            results = Email.get_statistics_range_by_dates(**query_params)

            data = {
                'statistic': statistic,
                'results': results,
            }
            data = json.dumps(data)
            return HttpResponse(data, content_type='application/json')
        except Exception as e:
            logger.error(e)


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get(self, request, *args, **kwargs):
        try:
            perfil = Perfil.get_perfil(request.user)
            perfil.empresas = perfil.empresas.all().order_by('empresa')
            logger.info(perfil.usuario)
            data = {
                'perfil': perfil
            }
            return render(request, self.template_name, data)
        except Exception as e:
            logger.error(e)
            return HttpResponse("No autorizado")
