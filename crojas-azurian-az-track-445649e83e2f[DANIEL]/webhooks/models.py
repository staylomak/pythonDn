# -*- coding: utf-8 -*-


from __future__ import unicode_literals


import logging


from django.db import models


from configuraciones.models import GeneralConfiguration


logger = logging.getLogger(__name__)


class EmailLogEvent(models.Model):
    input_date = models.DateField(auto_now_add=True)
    empresa = models.CharField(max_length=120)
    correo = models.EmailField(max_length=250)
    numero_folio = models.BigIntegerField()
    tipo_dte = models.IntegerField()
    rut_emisor = models.CharField(max_length=250)
    resolucion_emisor = models.BigIntegerField(null=True)
    fecha_evento = models.BigIntegerField()
    nombre_evento = models.CharField(max_length=250)

    def __unicode__(self):
        return u"{0} {1} {2} {3} {4}".format(
            self.input_date, self.correo, self.numero_folio,
            self.tipo_dte, self.nombre_evento)

    @classmethod
    def write_event(self, event, body):
        logger.info("Entrando a write_event de EmailLogEvent")
        config = GeneralConfiguration.get_configuration(body['empresa'])

        if config is not None and config.events_register:
            events = (config.events_to_register).split(';')
            logger.info(events)
            logger.info(event)

            for ev in events:
                if ev == event:
                    log_event = EmailLogEvent.objects.create(
                        empresa=body['empresa'],
                        correo=body['email'],
                        numero_folio=body['numero_folio'],
                        tipo_dte=body['tipo_dte'],
                        rut_emisor=body['rut_emisor'],
                        resolucion_emisor=body['resolucion_emisor'],
                        fecha_evento=body['timestamp'],
                        nombre_evento=event,
                    )
                    log_event.save()

    @classmethod
    def get_count_by_months(self, date_from, date_to, empresa):
        params = dict()
        params['input_date__range'] = (date_from, date_to)
        params['empresa'] = empresa
        return EmailLogEvent.objects.filter(**params).count()
