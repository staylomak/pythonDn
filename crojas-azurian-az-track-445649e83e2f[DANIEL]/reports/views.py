# -*- coding: utf-8 -*-


from datetime import datetime
import json
import logging
from StringIO import StringIO
from zipfile import ZipFile, ZIP_DEFLATED


from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView


from .tasks import export_task, get_report_file_format
from autenticacion.views import LoginRequiredMixin
from configuraciones.models import GeneralConfiguration
from emails.models import Email
from perfiles.models import Perfil
from utils.generics import get_date_to_string
from utils.tablib_export import create_tablib


logger = logging.getLogger(__name__)


class ReporteConsolidadoTemplateView(LoginRequiredMixin, TemplateView):
    """ Esta vista esta creada para extraer reportes consoliados
        dentro de algun periodo de tiempo en base a un rango de fechas
        desde - hasta
    """

    def get(self, request, *args, **kwargs):
        perfil = Perfil.get_perfil(request.user)
        logger.info(perfil)
        data = {
            'es_admin': perfil.es_admin,
            'empresas': perfil.empresas.all(),
        }
        return render(request, 'reports/consolidados.html', data)

    def post(self, request, *args, **kwargs):
        date_from = request.POST['date_from']
        date_to = request.POST['date_to']
        empresa = request.POST['empresas']
        date_from = datetime.strptime(str(date_from), '%d/%m/%Y')
        date_to = datetime.strptime(str(date_to), '%d/%m/%Y')
        empresa = str(empresa)
        data = Email.get_emails_by_dates(date_from, date_to, empresa)
        report_file = create_tablib(data, empresa)

        report_file_format = get_report_file_format(empresa)

        if report_file_format == 'xlsx':
            response_file = report_file.xlsx
            response_filename = 'consolidado' + get_date_to_string() + report_file_format
            response_filetype = 'application/vnd.ms-excel'
        elif report_file_format == 'tsv':
            response_file = report_file.tsv
            response_filename = 'consolidado' + get_date_to_string() + report_file_format
            response_filetype = 'text/tsv'
        else:
            response_file = report_file.csv
            response_filename = 'consolidado' + get_date_to_string() + report_file_format
            response_filetype = 'text/csv'

        general_conf = GeneralConfiguration.get_configuration(empresa)

        if general_conf is not None and general_conf.report_file_zipped:
            # ejecutar proceso de comprimir reporte
            in_memory = StringIO()

            with ZipFile(in_memory, 'w') as archive:
                archive.writestr(response_filename, str(response_file), ZIP_DEFLATED)

            response = HttpResponse(in_memory.getvalue(), content_type="application/x-zip-compressed")
            response['Content-Disposition'] = 'attachment; filename="reporte.zip"'
            return response
        else:
            # retornar el reporte
            response = HttpResponse(response_file, content_type=response_filetype)
            response['Content-Disposition'] = 'attachment; filename="' + response_filename + '"'
            return response


class DynamicReportTemplateView(LoginRequiredMixin, TemplateView):
    def get(self, request, date_from, date_to, empresa,
            correo, folio, rut, mount_from, mount_to, fallidos,
                                    op1, op2, op3, *args, **kwargs):
        parameters = dict()
        # preparación de parámetros
        date_from = int(date_from, base=10)
        date_to = int(date_to, base=10)
        parameters['date_from'] = date_from
        parameters['date_to'] = date_to
        if empresa == 'all':
            empresa = None
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

        report_file_format = get_report_file_format(empresa)

        context = dict()
        context['user_email'] = request.user.email
        context['file_name'] = 'reporte_dinamico' + get_date_to_string()\
                               + report_file_format
        context['export_type'] = 'export_dynamic_emails'
        context['empresa'] = empresa
        context['params'] = json.dumps(parameters)
        export_task(**context)
        data = json.dumps({"status": "ok"})
        return HttpResponse(data, content_type="application/json")


class GeneralReportTemplateView(LoginRequiredMixin, TemplateView):

    def get(self, request, date_from, date_to, empresa,
                                        tipo_receptor, *args, **kwargs):
        try:
            if date_from and date_to:
                context = {
                    'date_from': str(date_from),
                    'date_to': str(date_to),
                    'empresa': str(empresa),
                    'tipo_receptor': tipo_receptor,
                    'user_email': request.user.email,
                    'file_name': 'reporte_general' + get_date_to_string()
                                 + get_report_file_format(empresa),
                    'export_type': 'export_general_email',
                }
                export_task(**context)
                data = json.dumps({"status": "ok"})
                return HttpResponse(data, content_type="application/json")
        except Exception, e:
            print e
            logger.error(e)
            return HttpResponse()


class SendedReportTemplateView(LoginRequiredMixin, TemplateView):

    def get(self, request, date_from, date_to,
            empresa, tipo_receptor, *args, **kwargs):
        try:
            if date_from and date_to:
                context = {
                    'date_from': str(date_from),
                    'date_to': str(date_to),
                    'empresa': str(empresa),
                    'tipo_receptor': tipo_receptor,
                    'user_email': request.user.email,
                    'file_name': 'reporte_enviados' + get_date_to_string()
                                 + get_report_file_format(empresa),
                    'export_type': 'export_sended_email',
                }
            export_task(**context)
            data = json.dumps({"status": "ok"})
            return HttpResponse(data, content_type="application/json")
        except Exception, e:
            logger.error(e)
            return HttpResponse()


class FailureReportTemplateView(LoginRequiredMixin, TemplateView):

    def get(self, request, date_from, date_to, empresa,
                                    tipo_receptor, *args, **kwargs):
        try:
            if date_from and date_to:
                context = {
                    'date_from': str(date_from),
                    'date_to': str(date_to),
                    'empresa': str(empresa),
                    'tipo_receptor': str(tipo_receptor),
                    'user_email': request.user.email,
                    'file_name': 'reporte_fallidos' + get_date_to_string()
                                 + get_report_file_format(empresa),
                    'export_type': 'export_failure_email',
                }
            export_task(**context)
            data = json.dumps({"status": "ok"})
            return HttpResponse(data, content_type="application/json")
        except Exception, e:
            logger.error(e)
            return HttpResponse()
