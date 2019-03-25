# -*- coding: utf-8 -*-


from __future__ import unicode_literals


import json
import logging


from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models import Count, Q, Case, When, Sum, IntegerField, Value


from boto.gs.connection import GSConnection


from configuraciones.models import GeneralConfiguration
from empresas.models import Empresa
from tipodocumentos.models import TipoDocumento
from utils.generics import timestamp_to_date, to_unix_timestamp


MAX_QUERY_LENGTH = 10000


logger = logging.getLogger(__name__)


class FileQuerySet(models.QuerySet):
    """ Clase encargada de eliminar los adjuntos en casos de
        DELETEs masivos
    """

    def delete(self, *args, **kwargs):
        try:
            logger.info("Intentado eliminar archivos del bucket GCS")
            logger.info("Para el QuerySet Email")
            conn = GSConnection(settings.GS_ACCESS_KEY_ID, settings.GS_SECRET_ACCESS_KEY)
            bucket = conn.get_bucket(settings.GS_BUCKET_NAME)

            for obj in self:
                if obj.xml.name != '':
                    logger.info("borrando xml")
                    bucket.delete_key(obj.xml)
                if obj.pdf.name != '':
                    logger.info("borrando pdf")
                    bucket.delete_key(obj.pdf)
                if obj.adjunto1.name != '':
                    logger.info("borrando adjunto1")
                    bucket.delete_key(obj.adjunto1)
                logger.info("Archivos eliminados")
        except Exception as e:
            logger.error("Error al intentar eliminar archivo del GCS")
            logger.error(e)
        finally:
            logger.info("Borrando QuerySet")
            super(FileQuerySet, self).delete(*args, **kwargs)
            logger.info("QuerySet eliminado")


class Email(models.Model):
    # campos basicos
    input_date = models.DateField(auto_now_add=True, db_index=True)
    # campos dte
    empresa = models.ForeignKey(Empresa)
    rut_receptor = models.CharField(max_length=20, db_index=True)
    rut_emisor = models.CharField(max_length=20, db_index=True)
    tipo_envio = models.CharField(max_length=20, db_index=True)
    tipo_dte = models.ForeignKey(TipoDocumento)
    numero_folio = models.BigIntegerField(db_index=True)
    resolucion_receptor = models.IntegerField(null=True, blank=True)
    resolucion_emisor = models.IntegerField(null=True, blank=True)
    monto = models.BigIntegerField(default=0, db_index=True)
    fecha_emision = models.BigIntegerField(null=True, blank=True)
    fecha_recepcion = models.BigIntegerField(null=True, blank=True)
    estado_documento = models.CharField(max_length=100, null=True, blank=True)
    tipo_operacion = models.CharField(max_length=100, null=True, blank=True)
    tipo_receptor = models.CharField(max_length=100, null=True, blank=True)
    id_envio = models.BigIntegerField(blank=True, null=True, db_index=True)
    # campos correo
    nombre_cliente = models.CharField(max_length=200)
    correo = models.EmailField(max_length=250, db_index=True)
    asunto = models.CharField(max_length=200, blank=True, null=True)
    html = models.TextField(blank=True, null=True)
    # campos adicionales
    opcional1 = models.CharField(max_length=255, null=True, db_index=True)
    opcional2 = models.CharField(max_length=255, null=True, db_index=True)
    opcional3 = models.CharField(max_length=255, null=True, db_index=True)
    # adjuntos
    xml = models.FileField(
        upload_to='adjuntos/xml/%Y/%m/%d/%H%M%S', null=True, blank=True)
    pdf = models.FileField(
        upload_to='adjuntos/pdf/%Y/%m/%d/%H%M%S', null=True, blank=True)
    adjunto1 = models.FileField(
        upload_to='adjuntos/ad1/%Y/%m/%d/%H%M%S', null=True, blank=True)
    # campos de processed
    smtp_id = models.CharField(max_length=200, null=True, blank=True)
    processed_date = models.BigIntegerField(null=True, blank=True)
    processed_event = models.CharField(max_length=240,
                                       null=True,
                                       blank=True,
                                       db_index=True)
    processed_sg_event_id = models.CharField(max_length=240,
                                             null=True,
                                             blank=True)
    processed_sg_message_id = models.CharField(max_length=240,
                                               null=True,
                                               blank=True)
    # campos delivered
    delivered_date = models.BigIntegerField(null=True, blank=True)
    delivered_event = models.CharField(max_length=240,
                                       null=True,
                                       blank=True,
                                       db_index=True)
    delivered_sg_event_id = models.CharField(max_length=240,
                                             null=True,
                                             blank=True)
    delivered_sg_message_id = models.CharField(max_length=240,
                                               null=True,
                                               blank=True)
    delivered_response = models.TextField(null=True, blank=True)
    # campos open
    opened_first_date = models.BigIntegerField(null=True, blank=True)
    opened_last_date = models.BigIntegerField(null=True, blank=True)
    opened_event = models.CharField(max_length=240,
                                    null=True,
                                    blank=True,
                                    db_index=True)
    opened_ip = models.CharField(max_length=100, null=True, blank=True)
    opened_user_agent = models.CharField(max_length=255,
                                         null=True,
                                         blank=True)
    opened_sg_event_id = models.CharField(max_length=240,
                                          null=True,
                                          blank=True)
    opened_sg_message_id = models.CharField(max_length=240,
                                            null=True,
                                            blank=True)
    opened_count = models.IntegerField(null=True,
                                       blank=True,
                                       default=0)
    # campos dropped
    dropped_date = models.BigIntegerField(null=True, blank=True)
    dropped_sg_event_id = models.CharField(max_length=240,
                                           null=True,
                                           blank=True)
    dropped_sg_message_id = models.CharField(max_length=240,
                                             null=True,
                                             blank=True)
    dropped_reason = models.CharField(max_length=240, null=True, blank=True)
    dropped_event = models.CharField(max_length=240,
                                     null=True,
                                     blank=True,
                                     db_index=True)
    # campos bounce
    bounce_date = models.BigIntegerField(null=True, blank=True)
    bounce_event = models.CharField(max_length=240,
                                    null=True,
                                    blank=True,
                                    db_index=True)
    bounce_sg_event_id = models.CharField(max_length=240,
                                          null=True,
                                          blank=True)
    bounce_sg_message_id = models.CharField(max_length=240,
                                            null=True,
                                            blank=True)
    bounce_reason = models.TextField(null=True, blank=True)
    bounce_status = models.CharField(max_length=240, null=True, blank=True)
    bounce_type = models.CharField(max_length=240, null=True, blank=True)
    # campos unscribes
    unsubscribe_date = models.BigIntegerField(null=True, blank=True)
    unsubscribe_uid = models.CharField(max_length=240, null=True, blank=True)
    unsubscribe_purchase = models.CharField(max_length=240,
                                            null=True,
                                            blank=True)
    unsubscribe_id = models.CharField(max_length=240, null=True, blank=True)
    unsubscribe_event = models.CharField(max_length=240,
                                         null=True,
                                         blank=True,
                                         db_index=True)
    # campos click
    click_ip = models.CharField(max_length=100, null=True, blank=True)
    click_purchase = models.CharField(max_length=240, null=True, blank=True)
    click_useragent = models.CharField(max_length=255, null=True, blank=True)
    click_event = models.CharField(max_length=240,
                                   null=True,
                                   blank=True,
                                   db_index=True)
    click_email = models.CharField(max_length=240, null=True, blank=True)
    click_date = models.BigIntegerField(null=True, blank=True)
    click_url = models.CharField(max_length=240, null=True, blank=True)

    # metodos manager al objects
    objects = FileQuerySet.as_manager()

    def __unicode__(self):
        return u"{0} - {1}".format(self.correo, self.numero_folio)

    def delete(self, *args, **kwargs):
        try:
            logger.info("Intentado eliminar archivos del bucket GCS")
            logger.info("Para el objeto Email")
            conn = GSConnection(settings.GS_ACCESS_KEY_ID, settings.GS_SECRET_ACCESS_KEY)
            bucket = conn.get_bucket(settings.GS_BUCKET_NAME)

            if self.xml.name != '':
                logger.info("borrando xml")
                bucket.delete_key(self.xml)
            if self.pdf.name != '':
                logger.info("borrando pdf")
                bucket.delete_key(self.pdf)
            if self.adjunto1.name != '':
                logger.info("borrando adjunto1")
                bucket.delete_key(self.adjunto1)
            logger.info("Archivos Eliminados")
        except Exception as e:
            logger.error("Error al intentar eliminar archivo del GCS")
            logger.error(e)
        finally:
            logger.info("Borrando objeto")
            super(Email, self).delete(*args, **kwargs)
            logger.info("Eliminado")

    # funcion utilizada desde el webhook rest
    @classmethod
    def get_email_by_id(self, email_id):
        try:
            email = Email.objects.get(pk=email_id)
            logger.info("Email Existe")
        except Email.DoesNotExist:
            logger.error("Email.DoesNotExist")
            email = None
        return email

    # funcion DRY para webhook api
    @classmethod
    def set_default_fields(self, body):
        empresa_id = str(body['empresa']).decode('utf-8')
        rut_receptor = str(body['rut_receptor']).decode('utf-8')
        rut_emisor = str(body['rut_emisor']).decode('utf-8')
        tipo_envio = str(body['tipo_envio']).decode('utf-8')
        tipo_dte_id = body['tipo_dte']
        numero_folio = body['numero_folio']

        try:
            resolucion_receptor = body['resolucion_receptor']
            if resolucion_receptor == '' or None:
                resolucion_receptor = None
        except:
            resolucion_receptor = None

        resolucion_emisor = body['resolucion_emisor']
        monto = body['monto']

        fecha_emision = body['fecha_emision']
        if fecha_emision == '' or None:
            fecha_emision = 0
        else:
            fecha_emision = to_unix_timestamp(fecha_emision)

        try:
            fecha_recepcion = body['fecha_recepcion']
            if fecha_recepcion == '' or None:
                fecha_recepcion = None
            else:
                fecha_recepcion = to_unix_timestamp(fecha_recepcion)
        except:
            fecha_recepcion = None

        estado_documento = str(body['estado_documento']).decode('utf-8')
        tipo_operacion = str(body['tipo_operacion']).decode('utf-8')
        tipo_receptor = str(body['tipo_receptor']).decode('utf-8')
        nombre_cliente = body['nombre_cliente']
        correo = str(body['email']).decode('utf-8')
        id_envio = str(body['id_envio']).decode('utf-8')

        # parametros opcionales
        try:
            opcional1 = str(body['opcional1']).decode('utf-8')
        except:
            opcional1 = None
        try:
            opcional2 = str(body['opcional2']).decode('utf-8')
        except:
            opcional2 = None
        try:
            opcional3 = str(body['opcional3']).decode('utf-8')
        except:
            opcional3 = None

        if id_envio == '' or None:
            id_envio = None
        else:
            id_envio = int(id_envio, base=10)

        email = Email.objects.create(
            empresa_id=empresa_id,
            rut_receptor=rut_receptor,
            rut_emisor=rut_emisor,
            tipo_envio=tipo_envio,
            tipo_dte_id=tipo_dte_id,
            numero_folio=numero_folio,
            resolucion_receptor=resolucion_receptor,
            resolucion_emisor=resolucion_emisor,
            monto=monto,
            fecha_emision=fecha_emision,
            fecha_recepcion=fecha_recepcion,
            estado_documento=estado_documento,
            tipo_operacion=tipo_operacion,
            tipo_receptor=tipo_receptor,
            nombre_cliente=nombre_cliente,
            correo=correo,
            id_envio=id_envio,
            opcional1=opcional1,
            opcional2=opcional2,
            opcional3=opcional3
        )
        return email

    @classmethod
    def get_statistics_count_by_dates(self, date_from, date_to,
                                      empresa, tipo_receptor='all'):
        query_params = dict()
        query_params['input_date__range'] = (date_from, date_to)
        query_params['empresa'] = empresa
        if tipo_receptor != 'all':
            query_params['tipo_receptor'] = tipo_receptor

        statistics = Email.objects.filter(
            **query_params
        ).aggregate(
            total=Count('input_date'),
            delivered=Sum(
                Case(
                    When(delivered_event='delivered', then=1),
                    default=Value(0),
                    output_field=IntegerField(),
                ),
            ),
            opened=Sum(
                Case(
                    When(opened_event='open', then=1),
                    default=Value(0),
                    output_field=IntegerField(),
                ),
            ),
            dropped=Sum(
                Case(
                    When(dropped_event='dropped', then=1),
                    default=Value(0),
                    output_field=IntegerField(),
                ),
            ),
            bounced=Sum(
                Case(
                    When(bounce_event='bounce', then=1),
                    default=Value(0),
                    output_field=IntegerField(),
                ),
            ),
        )
        return statistics

    @classmethod
    def get_statistics_range_by_dates(self, date_from, date_to,
                                      empresa, tipo_receptor='all'):
        query_params = dict()
        query_params['input_date__range'] = (date_from, date_to)
        query_params['empresa'] = empresa
        if tipo_receptor != 'all':
            query_params['tipo_receptor'] = tipo_receptor

        emails = Email.objects.filter(
            **query_params
        ).values('input_date').annotate(
            total=Count('input_date'),
            processed=Count('processed_event'),
            delivered=Count('delivered_event'),
            opened=Count('opened_event'),
            dropped=Count('dropped_event'),
            bounced=Count('bounce_event')
        ).order_by('input_date')

        data = list()
        for email in emails:
            email = json.dumps(email, cls=DjangoJSONEncoder)
            data.append(json.loads(email))
        return data

    @classmethod
    def delete_old_emails_by_date(self, date_to_delete, empresa):
        try:
            emails = Email.objects.filter(
                input_date__lt=date_to_delete,
                empresa=empresa,
            )
            if emails.count() > 0:
                logger.info('Cantidad de correos a eliminar: %d' % emails.count())
                emails.delete()
            else:
                logger.info('No hay correos para eliminar')
        except Exception, e:
            logger.error(e)

    @classmethod
    def get_emails_by_dynamic_query(self, date_from, date_to, empresa, correo,
                                    folio, rut, mount_from, mount_to, fallidos,
                                    opcional1, opcional2, opcional3,
                                    display_start, display_length):
        if folio is not None:
            logger.info("query de folio con empresa")
            emails = Email.objects.filter(
                empresa=empresa, numero_folio=folio
            ).select_related().order_by('-input_date')
        elif fallidos is True:
            logger.info("query de fallidos")
            emails = Email.objects.filter(
                Q(input_date__range=(date_from, date_to)),
                Q(empresa=empresa),
                Q(bounce_event='bounce') | Q(dropped_event='dropped')
            ).select_related().order_by('-input_date')
        else:
            params = dict()
            logger.info("query dinamica")
            params['input_date__range'] = (date_from, date_to)
            params['empresa'] = empresa
            if correo is not None:
                logger.info("con correo")
                params['correo'] = correo
            if rut is not None:
                logger.info("con rut receptor")
                params['rut_receptor'] = rut
            if mount_from is not None and mount_to is not None:
                logger.info("con rango montos")
                params['monto__range'] = (mount_from, mount_to)
            if opcional1 is not None:
                logger.info("con campo opcional1")
                params['opcional1'] = opcional1
            if opcional2 is not None:
                logger.info("con campo opcional2")
                params['opcional2'] = opcional2
            if opcional3 is not None:
                logger.info("con campo opcional3")
                params['opcional3'] = opcional3
            emails = Email.objects.filter(
                **params
            ).select_related().order_by('-input_date')

        # imprimir consulta
        logger.info("query")
        logger.info(emails.query)

        # despues de consultar paginar y preparar retorno de emails
        query_total = emails.count()
        logger.info(query_total)

        if display_start is 0:
            emails = emails[display_start:display_length]
        else:
            emails = emails[display_start:display_length + display_start]
        if emails:
            query_length = emails.count()
        else:
            query_length = 0
        return {
            'query_total': query_total,
            'query_length': query_length,
            'data': emails,
        }

    @classmethod
    def get_emails_by_dynamic_query_async(self, date_from, date_to, empresa,
                          correo, folio, rut, mount_from, mount_to, fallidos,
                                            opcional1, opcional2, opcional3):

        date_from = timestamp_to_date(date_from)
        date_to = timestamp_to_date(date_to)

        if folio is not None:
            logger.info("query de folio con empresa")
            emails = Email.objects.filter(
                empresa=empresa, numero_folio=folio
            ).select_related().order_by('-input_date')
        elif fallidos is True:
            logger.info("query de fallidos")
            emails = Email.objects.filter(
                Q(input_date__range=(date_from, date_to)),
                Q(empresa=empresa),
                Q(bounce_event='bounce') | Q(dropped_event='dropped')
            ).select_related().order_by('-input_date')
        else:
            params = dict()
            logger.info("query dinamica")
            if date_from and date_to:
                params['input_date__range'] = (date_from, date_to)
            if empresa is not None:
                logger.info("con empresa")
                params['empresa'] = empresa
            if correo is not None:
                logger.info("con correo")
                params['correo'] = correo
            if rut is not None:
                logger.info("con rut receptor")
                params['rut_receptor'] = rut
            if mount_from is not None and mount_to is not None:
                logger.info("con montos")
                params['monto__range'] = (mount_from, mount_to)
            if opcional1 is not None:
                logger.info("con campo opcional1")
                params['opcional1'] = opcional1
            if opcional2 is not None:
                logger.info("con campo opcional2")
                params['opcional2'] = opcional2
            if opcional3 is not None:
                logger.info("con campo opcional3")
                params['opcional3'] = opcional3
            emails = Email.objects.filter(
                **params
            ).select_related().order_by('-input_date')

        # imprimir consulta
        logger.info("query")
        logger.info(emails.query)

        # despues de consultar paginar y preparar retorno de emails
        query_total = emails.count()
        logger.info(query_total)

        # retornar emails
        if emails:
            return emails
        else:
            return None

    @classmethod
    def get_emails_by_dates_async(self, date_from, date_to,
                                  empresa, tipo_receptor='all'):
        params = dict()
        params['input_date__range'] = (date_from, date_to)
        if empresa != 'all':
            params['empresa'] = empresa
        if tipo_receptor != 'all':
            params['tipo_receptor'] = tipo_receptor

        emails = Email.objects.filter(
            **params
        ).select_related().order_by('input_date')[:self.get_max_query_length(empresa)]
        if emails:
            return emails
        else:
            return None

    @classmethod
    def get_emails_by_dates(self, date_from, date_to, empresa):
        params = dict()
        params['input_date__range'] = (date_from, date_to)
        params['empresa'] = empresa
        emails = Email.objects.filter(
            **params
        ).select_related().order_by('input_date')
        logger.info(emails.query)
        logger.info(emails.count())
        if emails:
            return emails
        else:
            return None

    @classmethod
    def get_sended_emails_by_dates_async(self, date_from, date_to,
                                         empresa, tipo_receptor='all'):
        params = dict()
        params['input_date__range'] = (date_from, date_to)
        params['delivered_event'] = 'delivered'
        if empresa != 'all':
            params['empresa'] = empresa
        if tipo_receptor != 'all':
            params['tipo_receptor'] = tipo_receptor

        emails = Email.objects.filter(
            **params
        ).select_related().order_by('input_date')[:self.get_max_query_length(empresa)]
        if emails:
            return emails
        else:
            return None

    @classmethod
    def get_failure_emails_by_dates_async(self, date_from, date_to,
                                          empresa, tipo_receptor):
        if tipo_receptor == 'all':
            logger.info('Todos los tipos de receptores')
            emails = Email.objects.filter(
                Q(input_date__range=(date_from, date_to)),
                Q(empresa=empresa),
                Q(bounce_event='bounce') | Q(dropped_event='dropped')
            )
        else:
            logger.info('Sólo el tipo de receptor ' + tipo_receptor)
            emails = Email.objects.filter(
                Q(input_date__range=(date_from, date_to)),
                Q(tipo_receptor=tipo_receptor), Q(empresa=empresa),
                Q(bounce_event='bounce') | Q(dropped_event='dropped')
            )
        emails = emails.select_related().order_by('input_date')[:self.get_max_query_length(empresa)]
        logger.info(emails.query)
        logger.info(emails.count())
        if emails.count() > 0:
            return emails
        else:
            return None

    @classmethod
    def get_max_query_length(self, empresa):
        conf = GeneralConfiguration.get_configuration(empresa)
        if conf is not None:
            return conf.report_row_max_length
        else:
            return MAX_QUERY_LENGTH


    @classmethod
    def get_email(self, correo, numero_folio, tipo_dte, rut_emisor,
                  resolucion_emisor, id_envio, tipo_receptor=None):
        if isinstance(numero_folio, (str, basestring)):
            numero_folio = int(numero_folio, base=10)
        if isinstance(tipo_dte, (str, basestring)):
            tipo_dte = int(tipo_dte, base=10)
        if isinstance(resolucion_emisor, (str, basestring)):
            resolucion_emisor = int(resolucion_emisor, base=10)
        if isinstance(id_envio, (str, basestring)):
            id_envio = int(id_envio, base=10)

        query_params = dict()
        query_params['correo'] = correo
        query_params['numero_folio'] = numero_folio
        query_params['tipo_dte_id'] = tipo_dte
        query_params['rut_emisor'] = rut_emisor
        query_params['resolucion_emisor'] = resolucion_emisor
        query_params['id_envio'] = id_envio

        if tipo_receptor is not None:
            query_params['tipo_receptor'] = tipo_receptor

        try:
            email = Email.objects.filter(
                **query_params
            ).select_related().order_by('-input_date')[:1]
            logger.info(email)
            logger.info(len(email))
            logger.info(email.query)

            if len(email) > 0:
                return email[0]
            else:
                return None
        except Exception, e:
            logger.error(e)
            return None

    @classmethod
    def get_emails_no_delivered(self, rut_empresa=None):
        if rut_empresa is not None:
            emails = Email.objects.filter(
                Q(empresa=rut_empresa),
                Q(processed_event__isnull=True) & Q(dropped_event__isnull=True)
            ).order_by('id')
        else:
            emails = Email.objects.filter(
                Q(processed_event__isnull=True) & Q(dropped_event__isnull=True)
            ).order_by('id')
        if emails:
            logger.info("se encontraron la siguente cantidad de emails pendientes")
            logger.info(emails.count())
            return emails
        else:
            logger.info("No se encontraron emails pendientes de envío")
            return None
