# -*- coding: utf-8 -*-


import logging


from app import celery_app


logger = logging.getLogger(__name__)


@celery_app.task
def soap_ws_task(soap_obj):
    logger.info("Entrando al Task de SoapWS")
    logger.info(soap_obj)
    soap_obj.execute()


@celery_app.task
def rest_ws_task(**kwargs):
    logger.info("Entrando al Task de RestWS")
    logger.info(kwargs)
