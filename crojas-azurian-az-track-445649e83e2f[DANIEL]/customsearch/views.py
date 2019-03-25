# -*- coding: utf-8 -*-


import logging


from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView


from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView


from app import settings
from autenticacion.views import LoginRequiredMixin
from emails.models import Email
from emails.serializers import EmailTrackRelatedSerializer
from perfiles.models import Perfil
from utils.generics import timestamp_to_date


logger = logging.getLogger(__name__)


class DynamicQueryView(APIView):
    serializer_class = EmailTrackRelatedSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, date_from, date_to, empresa, correo, folio, rut,
            mount_from, mount_to, fallidos, op1, op2, op3, *args, **kwargs):
        parameters = dict()
        # preparación de parámetros
        date_from = int(date_from, base=10)
        date_to = int(date_to, base=10)
        date_from = timestamp_to_date(date_from)
        date_to = timestamp_to_date(date_to)
        parameters['date_from'] = date_from
        parameters['date_to'] = date_to
        parameters['empresa'] = empresa
        if correo == '-':
            correo = None
        parameters['correo'] = correo
        if folio == '-':
            folio = None
        parameters['folio'] = folio
        if rut == '-':
            rut = None
        parameters['rut'] = rut
        if mount_from == '-':
            mount_from = None
        else:
            mount_from = int(mount_from, base=10)
        parameters['mount_from'] = mount_from
        if mount_to == '-':
            mount_to = None
        else:
            mount_to = int(mount_to, base=10)
        parameters['mount_to'] = mount_to
        if fallidos == 'true':
            parameters['fallidos'] = True
        elif fallidos == 'false':
            parameters['fallidos'] = False
        else:
            parameters['fallidos'] = False
        if op1 == '-':
            parameters['opcional1'] = None
        else:
            parameters['opcional1'] = op1
        if op2 == '-':
            parameters['opcional2'] = None
        else:
            parameters['opcional2'] = op2
        if op3 == '-':
            parameters['opcional3'] = None
        else:
            parameters['opcional3'] = op3

        # preparación de parámetros de paginación
        echo = request.GET['sEcho']
        display_start = request.GET['iDisplayStart']
        display_length = request.GET['iDisplayLength']
        parameters['display_start'] = int(display_start, base=10)
        parameters['display_length'] = int(display_length, base=10)

        # ejecución de query dinamica
        emails = Email.get_emails_by_dynamic_query(**parameters)
        response = self.serializer_class(emails['data'], many=True)
        data = {
            'sEcho': echo,
            'data': response.data,
            'iTotalDisplayRecords': emails['query_total'],
            'iTotalRecords': emails['query_total'],
        }
        return Response(data)


class EmailDetailView(APIView):
    serializer_class = EmailTrackRelatedSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            pk = request.GET['pk']
            if pk:
                pk = int(pk, base=10)
                email = get_object_or_404(Email, pk=pk)
                if email is not None:
                    response = self.serializer_class(email, many=False)
                    return Response(response.data)
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(e)


class IndexTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'customsearch/index.html'

    def get(self, request, *args, **kwargs):
        try:
            perfil = Perfil.get_perfil(request.user)
            logger.info(perfil.usuario)
            bucket = settings.MEDIA_URL + settings.GS_BUCKET_NAME + '/'
            data = {
                'bucket': bucket,
                'perfil': perfil
            }
            return render(request, self.template_name, data)
        except Exception as e:
            logger.error(e)
            return HttpResponse("No autorizado")
