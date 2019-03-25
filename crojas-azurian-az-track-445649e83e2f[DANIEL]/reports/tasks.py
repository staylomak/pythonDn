# -*- coding: utf-8 -*-


from StringIO import StringIO
from zipfile import ZipFile, ZIP_DEFLATED
import json
import logging


from app import celery_app
from configuraciones.models import GeneralConfiguration
from emails.models import Email
from utils.generics import timestamp_to_date
from utils.sendgrid_client import EmailClient
from utils.tablib_export import create_tablib


logger = logging.getLogger(__name__)


def get_report_file_format(empresa_id):
    configuration = GeneralConfiguration.get_configuration(empresa_id)
    if configuration is not None:
        return configuration.report_file_format
    else:
        return "xlsx"


@celery_app.task
def export_task(**kwargs):
    logger.info(kwargs)
    export_type = kwargs['export_type']
    if export_type == 'export_general_email':
        tipo_receptor = kwargs['tipo_receptor']
        empresa = kwargs['empresa']
        user_email = kwargs['user_email']
        file_name = kwargs['file_name']
        date_from = kwargs['date_from']
        date_to = kwargs['date_to']
        date_from = int(date_from, base=10)
        date_to = int(date_to, base=10)
        date_from = timestamp_to_date(date_from)
        date_to = timestamp_to_date(date_to)
        params = dict()
        params['date_from'] = date_from
        params['date_to'] = date_to
        params['empresa'] = empresa
        params['tipo_receptor'] = tipo_receptor
        # Consulta
        data = Email.get_emails_by_dates_async(**params)
    elif export_type == 'export_sended_email':
        tipo_receptor = kwargs['tipo_receptor']
        empresa = kwargs['empresa']
        user_email = kwargs['user_email']
        file_name = kwargs['file_name']
        date_from = kwargs['date_from']
        date_to = kwargs['date_to']
        date_from = int(date_from, base=10)
        date_to = int(date_to, base=10)
        date_from = timestamp_to_date(date_from)
        date_to = timestamp_to_date(date_to)
        params = dict()
        params['date_from'] = date_from
        params['date_to'] = date_to
        params['empresa'] = empresa
        params['tipo_receptor'] = tipo_receptor
        # Consulta
        data = Email.get_sended_emails_by_dates_async(**params)
    elif export_type == 'export_failure_email':
        tipo_receptor = kwargs['tipo_receptor']
        empresa = kwargs['empresa']
        user_email = kwargs['user_email']
        file_name = kwargs['file_name']
        date_from = kwargs['date_from']
        date_to = kwargs['date_to']
        date_from = int(date_from, base=10)
        date_to = int(date_to, base=10)
        date_from = timestamp_to_date(date_from)
        date_to = timestamp_to_date(date_to)
        params = dict()
        params['date_from'] = date_from
        params['date_to'] = date_to
        params['empresa'] = empresa
        params['tipo_receptor'] = tipo_receptor
        # Consulta
        data = Email.get_failure_emails_by_dates_async(**params)
    elif export_type == 'export_dynamic_emails':
        user_email = kwargs['user_email']
        empresa = kwargs['empresa']
        file_name = kwargs['file_name']
        params = kwargs['params']
        params = json.loads(params)
        logger.info(params)
        data = Email.get_emails_by_dynamic_query_async(**params)

    if data is not None:
        try:
            logger.info("Existen datos para reporte")
            # Creación del documento
            report_file = create_tablib(data, empresa)
            logger.info("Se ha creado el archivo tablib.")

            # evaluacion del formato del archivo reporte
            report_file_format = get_report_file_format(empresa)
            logger.info("Se va a exportar archivo en formato %s", report_file_format)

            if report_file_format == 'xlsx':
                response_file = report_file.xlsx
                response_filename = file_name
            elif report_file_format == 'tsv':
                response_file = report_file.tsv
                response_filename = file_name
            else:
                response_file = report_file.csv
                response_filename = file_name

            # evaluar si el archivo es comprimido en zip
            general_conf = GeneralConfiguration.get_configuration(empresa)
            logger.info("Se obtiene configuración General de la Empresa")
            logger.info(general_conf.__dict__)

            if general_conf is not None and general_conf.report_file_zipped:
                logger.info("Intentando comprimir archivo reporte")
                # ejecutar proceso de comprimir reporte
                in_memory = StringIO()

                with ZipFile(in_memory, 'w') as archive:
                    archive.writestr(response_filename, str(response_file), ZIP_DEFLATED)

                response_file = in_memory.getvalue()
                response_filename = file_name + '.zip'
                logger.info("Archivo comprimido exitosamente.")

            # Crear objeto para enviarlo por correo
            data = dict()
            data['name'] = response_filename
            data['report'] = response_file

            # preparación de parametros
            mail = EmailClient(empresa)
            mail.send_report_to_user_with_attach(user_email, data)
            logger.info("Reportes generado correctamente")
        except Exception as e:
            logger.error("Error al enviar correo reporte")
            logger.error(e)
    else:
        logger.info("No se crear el archivo reporte por consulta vacía.")
