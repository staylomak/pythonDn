# -*- coding: utf-8 -*-


from datetime import date, timedelta
import logging


from .models import Email
from app import celery_app
from configuraciones.models import EliminacionHistorico
from empresas.models import Empresa
from utils.sendgrid_client import EmailClient


logger = logging.getLogger(__name__)


@celery_app.task
def input_queue(email):
    logger.info("Entrando a la cola de envío de email.")
    try:
        email_client = EmailClient(email.empresa_id)
        email_client.enviar_correo_dte(email)
    except Exception as e:
        logger.error(e)


@celery_app.task
def send_emails_no_delivered(emails=None):
    logger.info("Entrando a la cola de envío de correos pendientes de envío.")
    if emails is None:
        emails = Email.get_emails_no_delivered()
    try:
        for email in emails:
            email_client = EmailClient(email.empresa_id)
            email_client.enviar_correo_dte(email)
            print "Correo :" + email.correo + " Folio :" + email.numero_folio + " Enviado."
            logger.info("Correo :" + email.correo + " Folio :" + email.numero_folio + " Enviado.")
    except Exception as e:
        print "Error en send_emails_no_delivered"
        print e
        logger.error("Error en send_emails_no_delivered")
        logger.error(e)


@celery_app.task
def cron_clean_emails_history():
    """ Método que si tiene habilitada la opción de eliminar correos antiguos
        antiguos (parametrizado en app configuraciones) lista los correos
        desde el numero de meses máximo a retener en la DB.
    """
    # Listar todas las configuraciones activas
    active_configs = EliminacionHistorico.objects.filter(activo=True)
    logger.info('Iniciando tarea de eliminar correos historicos')

    # Recorrer listado
    for config in active_configs:
        if config.activo:
            logger.info('Procesando Holding: %s' % config.holding.nombre)
            if config.dias_a_eliminar is not None:
                try:
                    # resta la fecha de hoy con los días a eliminar
                    today = date.today()
                    days = timedelta(days=config.dias_a_eliminar)
                    date_to_delete = today - days
                    # listar las empresas al holding que pertenece la conf actual
                    empresas = Empresa.objects.filter(holding=config.holding)
                    for empresa in empresas:
                        logger.info('Procesando Empresa: %s' % empresa.empresa)
                        # enviar la petición para borrar
                        Email.delete_old_emails_by_date(date_to_delete, empresa)
                except Exception as e:
                    logger.error(e)
    logger.info('Finalizando tarea de eliminar correos historicos')
