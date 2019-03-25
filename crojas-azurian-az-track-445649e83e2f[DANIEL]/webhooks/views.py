# -*- coding: utf-8 -*-


import json
import logging


from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView


from .models import EmailLogEvent
from emails.models import Email
from utils.ws_middleware import SoapMiddleware


logger = logging.getLogger(__name__)


class SendGridRestWebhookView(TemplateView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SendGridRestWebhookView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request_body = json.loads(request.body.decode('utf-8'))

        for body in request_body:
            logger.info(request_body)
            try:
                evento_sendgrid = str(body['event']).decode('utf-8')
                email_id = str(body['email_id']).decode('utf-8')
                logger.info(evento_sendgrid)
            except Exception, e:
                logger.error(e)
                return HttpResponse(e)

            try:
                if evento_sendgrid and email_id:
                    email_id = int(email_id, base=10)
                    logger.info("es un webhook para el tracking")

                    if evento_sendgrid == 'processed':
                        email = Email.get_email_by_id(email_id)

                        if email is not None:
                            logger.info(email)
                            email.smtp_id = str(body['smtp-id']).decode('utf-8')
                            email.processed_date = body['timestamp']
                            email.processed_event = evento_sendgrid
                            email.processed_sg_event_id = str(body['sg_event_id']).decode('utf-8')
                            email.processed_sg_message_id = str(body['sg_message_id']).decode('utf-8')
                            email.save()
                            soap_ws = SoapMiddleware(email.pk, evento_sendgrid)
                            soap_ws.evaluate()
                            # proceso de registrar eventos en tabla log
                            EmailLogEvent.write_event(evento_sendgrid, body)

                    elif evento_sendgrid == 'delivered':
                        email = Email.get_email_by_id(email_id)

                        if email is not None:
                            logger.info(email)
                            email.smtp_id = str(body['smtp-id']).decode('utf-8')
                            email.delivered_date = body['timestamp']
                            email.delivered_event = evento_sendgrid
                            email.delivered_sg_event_id = str(body['sg_event_id']).decode('utf-8')
                            email.delivered_sg_message_id = str(body['sg_message_id']).decode('utf-8')
                            email.delivered_response = str(body['response']).decode('utf-8')
                            email.save()
                            soap_ws = SoapMiddleware(email.pk, evento_sendgrid)
                            soap_ws.evaluate()
                            # proceso de registrar eventos en tabla log
                            EmailLogEvent.write_event(evento_sendgrid, body)

                    elif evento_sendgrid == 'open':
                        email = Email.get_email_by_id(email_id)

                        if email is not None:
                            logger.info(email)
                            if email.opened_first_date is None:
                                email.opened_first_date = body['timestamp']
                            email.opened_last_date = body['timestamp']
                            email.opened_event = evento_sendgrid
                            email.opened_ip = str(body['ip']).decode('utf-8')
                            email.opened_user_agent = str(body['useragent']).decode('utf-8')
                            email.opened_sg_event_id = str(body['sg_event_id']).decode('utf-8')
                            email.opened_sg_message_id = str(body['sg_message_id']).decode('utf-8')
                            email.opened_count += 1
                            email.save()
                            soap_ws = SoapMiddleware(email.pk, evento_sendgrid)
                            soap_ws.evaluate()
                            # proceso de registrar eventos en tabla log
                            EmailLogEvent.write_event(evento_sendgrid, body)

                    elif evento_sendgrid == 'dropped':
                        email = Email.get_email_by_id(email_id)

                        if email is not None:
                            logger.info(email)
                            email.smtp_id = str(body['smtp-id']).decode('utf-8')
                            email.dropped_date = body['timestamp']
                            email.dropped_sg_event_id = str(body['sg_event_id']).decode('utf-8')
                            email.dropped_sg_message_id = str(body['sg_message_id']).decode('utf-8')
                            email.dropped_reason = str(body['reason']).decode('utf-8')
                            email.dropped_event = evento_sendgrid
                            email.save()
                            soap_ws = SoapMiddleware(email.pk, evento_sendgrid)
                            soap_ws.evaluate()
                            # proceso de registrar eventos en tabla log
                            EmailLogEvent.write_event(evento_sendgrid, body)

                    elif evento_sendgrid == 'bounce':
                        email = Email.get_email_by_id(email_id)

                        if email is not None:
                            logger.info(email)
                            email.bounce_date = body['timestamp']
                            email.bounce_event = evento_sendgrid
                            email.bounce_sg_event_id = str(body['sg_event_id']).decode('utf-8')
                            email.bounce_sg_message_id = str(body['sg_message_id']).decode('utf-8')
                            email.bounce_reason = str(body['reason']).decode('utf-8')
                            email.bounce_status = str(body['status']).decode('utf-8')
                            email.bounce_type = str(body['type']).decode('utf-8')
                            email.save()
                            soap_ws = SoapMiddleware(email.pk, evento_sendgrid)
                            soap_ws.evaluate()
                            # proceso de registrar eventos en tabla log
                            EmailLogEvent.write_event(evento_sendgrid, body)

                    elif evento_sendgrid == 'unsubscribe':
                        email = Email.get_email_by_id(email_id)

                        if email is not None:
                            logger.info(email)
                            email.unsubscribe_date = body['timestamp']
                            email.unsubscribe_uid = str(body['uid']).decode('utf-8')
                            email.unsubscribe_purchase = str(body['purchase']).decode('utf-8')
                            email.unsubscribe_id = str(body['id']).decode('utf-8')
                            email.unsubscribe_event = evento_sendgrid
                            email.save()
                            soap_ws = SoapMiddleware(email.pk, evento_sendgrid)
                            soap_ws.evaluate()
                            # proceso de registrar eventos en tabla log
                            EmailLogEvent.write_event(evento_sendgrid, body)

                    elif evento_sendgrid == 'click':
                        email = Email.get_email_by_id(email_id)

                        if email is not None:
                            logger.info(email)
                            email.click_ip = str(body['ip']).decode('utf-8')
                            email.click_purchase = ''
                            email.click_useragent = str(body['useragent']).decode('utf-8')
                            email.click_event = evento_sendgrid
                            email.click_email = str(body['email']).decode('utf-8')
                            email.click_date = body['timestamp']
                            email.click_url = str(body['url']).decode('utf-8')
                            email.save()
                            soap_ws = SoapMiddleware(email.pk, evento_sendgrid)
                            soap_ws.evaluate()
                            # proceso de registrar eventos en tabla log
                            EmailLogEvent.write_event(evento_sendgrid, body)
                else:
                    logger.error("parametros incompletos, correo no corresponde.")
            except Exception, e:
                logger.error(e)
                return HttpResponse(e, status=500)
        return HttpResponse()


class SendGridApiWebhookView(TemplateView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SendGridApiWebhookView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request_body = json.loads(request.body.decode('utf-8'))

        for body in request_body:
            logger.info(body)
            try:
                evento_sendgrid = str(body['event']).decode('utf-8')
                correo = str(body['email']).decode('utf-8')
                numero_folio = str(body['numero_folio']).decode('utf-8')
                tipo_dte = str(body['tipo_dte']).decode('utf-8')
                rut_emisor = str(body['rut_emisor']).decode('utf-8')
                resolucion_emisor = str(body['resolucion_emisor']).decode('utf-8')
                empresa = str(body['empresa']).decode('utf-8')
                id_envio = str(body['id_envio']).decode('utf-8')
                tipo_receptor = str(body['tipo_receptor']).decode('utf-8')

                logger.info(evento_sendgrid)
            except Exception, e:
                logger.error(e)
                return HttpResponse(e)

            try:
                if evento_sendgrid and correo and numero_folio and tipo_dte and rut_emisor and resolucion_emisor and tipo_receptor:
                    correo = str(correo).lower()
                    numero_folio = int(numero_folio, base=10)
                    logger.info("es un webhook para el tracking")

                    if evento_sendgrid == 'processed':
                        email = Email.get_email(correo, numero_folio, tipo_dte, rut_emisor, resolucion_emisor, id_envio, tipo_receptor)
                        logger.info(email)

                        if email is not None:
                            email.smtp_id = str(body['smtp-id']).decode('utf-8')
                            email.processed_date = body['timestamp']
                            email.processed_event = evento_sendgrid
                            email.processed_sg_event_id = str(body['sg_event_id']).decode('utf-8')
                            email.processed_sg_message_id = str(body['sg_message_id']).decode('utf-8')
                            email.save()
                            # proceso intermedio de soap web service
                            soap_ws = SoapMiddleware(email.pk, evento_sendgrid)
                            soap_ws.evaluate()
                            # proceso de registrar eventos en tabla log
                            EmailLogEvent.write_event(evento_sendgrid, body)
                        else:
                            logger.info("paso else no existe")
                            e = Email.set_default_fields(body)
                            # parametros del evento
                            e.smtp_id = str(body['smtp-id']).decode('utf-8')
                            e.processed_date = body['timestamp']
                            e.processed_event = evento_sendgrid
                            e.processed_sg_event_id = str(body['sg_event_id']).decode('utf-8')
                            e.processed_sg_message_id = str(body['sg_message_id']).decode('utf-8')
                            e.save()
                            # proceso intermedio de soap web service
                            soap_ws = SoapMiddleware(e.pk, evento_sendgrid)
                            soap_ws.evaluate()
                            # proceso de registrar eventos en tabla log
                            EmailLogEvent.write_event(evento_sendgrid, body)

                    elif evento_sendgrid == 'delivered':
                        email = Email.get_email(correo, numero_folio, tipo_dte, rut_emisor, resolucion_emisor, id_envio, tipo_receptor)
                        logger.info(email)

                        if email is not None:
                            email.empresa_id = empresa
                            email.smtp_id = str(body['smtp-id']).decode('utf-8')
                            email.delivered_date = body['timestamp']
                            email.delivered_event = evento_sendgrid
                            email.delivered_sg_event_id = str(body['sg_event_id']).decode('utf-8')
                            email.delivered_sg_message_id = str(body['sg_message_id']).decode('utf-8')
                            email.delivered_response = str(body['response']).decode('utf-8')
                            email.save()
                            # proceso intermedio de soap web service
                            soap_ws = SoapMiddleware(email.pk, evento_sendgrid)
                            soap_ws.evaluate()
                            # proceso de registrar eventos en tabla log
                            EmailLogEvent.write_event(evento_sendgrid, body)
                        else:
                            e = Email.set_default_fields(body)
                            # parametros del evento
                            e.smtp_id = str(body['smtp-id']).decode('utf-8')
                            e.delivered_date = body['timestamp']
                            e.delivered_event = evento_sendgrid
                            e.delivered_sg_event_id = str(body['sg_event_id']).decode('utf-8')
                            e.delivered_sg_message_id = str(body['sg_message_id']).decode('utf-8')
                            e.delivered_response = str(body['response']).decode('utf-8')
                            e.save()
                            # proceso intermedio de soap web service
                            soap_ws = SoapMiddleware(e.pk, evento_sendgrid)
                            soap_ws.evaluate()
                            # proceso de registrar eventos en tabla log
                            EmailLogEvent.write_event(evento_sendgrid, body)

                    elif evento_sendgrid == 'open':
                        email = Email.get_email(correo, numero_folio, tipo_dte, rut_emisor, resolucion_emisor, id_envio, tipo_receptor)
                        logger.info(email)

                        if email is not None:
                            email.empresa_id = empresa
                            if email.opened_first_date is None:
                                email.opened_first_date = body['timestamp']
                            email.opened_last_date = body['timestamp']
                            email.opened_event = evento_sendgrid
                            email.opened_ip = str(body['ip']).decode('utf-8')
                            email.opened_user_agent = str(body['useragent']).decode('utf-8')
                            email.opened_sg_event_id = str(body['sg_event_id']).decode('utf-8')
                            email.opened_sg_message_id = str(body['sg_message_id']).decode('utf-8')
                            email.opened_count += 1
                            email.save()
                            # proceso intermedio de soap web service
                            soap_ws = SoapMiddleware(email.pk, evento_sendgrid)
                            soap_ws.evaluate()
                            # proceso de registrar eventos en tabla log
                            EmailLogEvent.write_event(evento_sendgrid, body)
                        else:
                            e = Email.set_default_fields(body)
                            # parametros del evento
                            if e.opened_first_date is None:
                                e.opened_first_date = body['timestamp']
                            e.opened_last_date = body['timestamp']
                            e.opened_event = evento_sendgrid
                            e.opened_ip = str(body['ip']).decode('utf-8')
                            e.opened_user_agent = str(body['useragent']).decode('utf-8')
                            e.opened_sg_event_id = str(body['sg_event_id']).decode('utf-8')
                            e.opened_sg_message_id = str(body['sg_message_id']).decode('utf-8')
                            e.opened_count += 1
                            e.save()
                            # proceso intermedio de soap web service
                            soap_ws = SoapMiddleware(e.pk, evento_sendgrid)
                            soap_ws.evaluate()
                            # proceso de registrar eventos en tabla log
                            EmailLogEvent.write_event(evento_sendgrid, body)

                    elif evento_sendgrid == 'dropped':
                        email = Email.get_email(correo, numero_folio, tipo_dte, rut_emisor, resolucion_emisor, id_envio, tipo_receptor)

                        if email is not None:
                            logger.info(email)
                            email.empresa_id = empresa
                            email.smtp_id = str(body['smtp-id']).decode('utf-8')
                            email.dropped_date = body['timestamp']
                            email.dropped_sg_event_id = str(body['sg_event_id']).decode('utf-8')
                            email.dropped_sg_message_id = str(body['sg_message_id']).decode('utf-8')
                            email.dropped_reason = str(body['reason']).decode('utf-8')
                            email.dropped_event = evento_sendgrid
                            email.save()
                            # proceso intermedio de soap web service
                            soap_ws = SoapMiddleware(email.pk, evento_sendgrid)
                            soap_ws.evaluate()
                            # proceso de registrar eventos en tabla log
                            EmailLogEvent.write_event(evento_sendgrid, body)
                        else:
                            e = Email.set_default_fields(body)
                            # parametros del evento
                            e.smtp_id = str(body['smtp-id']).decode('utf-8')
                            e.dropped_date = body['timestamp']
                            e.dropped_sg_event_id = str(body['sg_event_id']).decode('utf-8')
                            e.dropped_sg_message_id = str(body['sg_message_id']).decode('utf-8')
                            e.dropped_reason = str(body['reason']).decode('utf-8')
                            e.dropped_event = evento_sendgrid
                            e.save()
                            # proceso intermedio de soap web service
                            soap_ws = SoapMiddleware(e.pk, evento_sendgrid)
                            soap_ws.evaluate()
                            # proceso de registrar eventos en tabla log
                            EmailLogEvent.write_event(evento_sendgrid, body)

                    elif evento_sendgrid == 'bounce':
                        email = Email.get_email(correo, numero_folio, tipo_dte, rut_emisor, resolucion_emisor, id_envio, tipo_receptor)

                        if email is not None:
                            logger.info(email)
                            email.empresa_id = empresa
                            email.bounce_date = body['timestamp']
                            email.bounce_event = evento_sendgrid
                            email.bounce_sg_event_id = str(body['sg_event_id']).decode('utf-8')
                            email.bounce_sg_message_id = str(body['sg_message_id']).decode('utf-8')
                            email.bounce_reason = str(body['reason']).decode('utf-8')
                            email.bounce_status = str(body['status']).decode('utf-8')
                            email.bounce_type = str(body['type']).decode('utf-8')
                            email.save()
                            # proceso intermedio de soap web service
                            soap_ws = SoapMiddleware(email.pk, evento_sendgrid)
                            soap_ws.evaluate()
                            # proceso de registrar eventos en tabla log
                            EmailLogEvent.write_event(evento_sendgrid, body)
                        else:
                            e = Email.set_default_fields(body)
                            # parametros del evento
                            e.bounce_date = body['timestamp']
                            e.bounce_event = evento_sendgrid
                            e.bounce_sg_event_id = str(body['sg_event_id']).decode('utf-8')
                            e.bounce_sg_message_id = str(body['sg_message_id']).decode('utf-8')
                            e.bounce_reason = str(body['reason']).decode('utf-8')
                            e.bounce_status = str(body['status']).decode('utf-8')
                            e.bounce_type = str(body['type']).decode('utf-8')
                            e.save()
                            # proceso intermedio de soap web service
                            soap_ws = SoapMiddleware(e.pk, evento_sendgrid)
                            soap_ws.evaluate()
                            # proceso de registrar eventos en tabla log
                            EmailLogEvent.write_event(evento_sendgrid, body)

                    elif evento_sendgrid == 'unsubscribe':
                        email = Email.get_email(correo, numero_folio, tipo_dte, rut_emisor, resolucion_emisor, id_envio, tipo_receptor)

                        if email is not None:
                            logger.info(email)
                            email.empresa_id = empresa
                            email.unsubscribe_date = body['timestamp']
                            email.unsubscribe_uid = str(body['uid']).decode('utf-8')
                            email.unsubscribe_purchase = str(body['purchase']).decode('utf-8')
                            email.unsubscribe_id = str(body['id']).decode('utf-8')
                            email.unsubscribe_event = evento_sendgrid
                            email.save()
                            # proceso intermedio de soap web service
                            soap_ws = SoapMiddleware(email.pk, evento_sendgrid)
                            soap_ws.evaluate()
                            # proceso de registrar eventos en tabla log
                            EmailLogEvent.write_event(evento_sendgrid, body)
                        else:
                            e = Email.set_default_fields(body)
                            # parametros del evento
                            e.unsubscribe_date = body['timestamp']
                            e.unsubscribe_uid = str(body['uid']).decode('utf-8')
                            e.unsubscribe_purchase = str(body['purchase']).decode('utf-8')
                            e.unsubscribe_id = str(body['id']).decode('utf-8')
                            e.unsubscribe_event = evento_sendgrid
                            e.save()
                            # proceso intermedio de soap web service
                            soap_ws = SoapMiddleware(e.pk, evento_sendgrid)
                            soap_ws.evaluate()
                            # proceso de registrar eventos en tabla log
                            EmailLogEvent.write_event(evento_sendgrid, body)

                    elif evento_sendgrid == 'click':
                        email = Email.get_email(correo, numero_folio, tipo_dte, rut_emisor, resolucion_emisor, id_envio, tipo_receptor)

                        if email is not None:
                            logger.info(email)
                            email.empresa_id = empresa
                            email.click_ip = str(body['ip']).decode('utf-8')
                            email.click_purchase = ''
                            email.click_useragent = str(body['useragent']).decode('utf-8')
                            email.click_event = evento_sendgrid
                            email.click_email = str(body['email']).decode('utf-8')
                            email.click_date = body['timestamp']
                            email.click_url = str(body['url']).decode('utf-8')
                            email.save()
                            # proceso intermedio de soap web service
                            soap_ws = SoapMiddleware(email.pk, evento_sendgrid)
                            soap_ws.evaluate()
                            # proceso de registrar eventos en tabla log
                            EmailLogEvent.write_event(evento_sendgrid, body)
                        else:
                            e = Email.set_default_fields(body)
                            # parametros del evento
                            e.click_ip = str(body['ip']).decode('utf-8')
                            e.click_purchase = ''
                            e.click_useragent = str(body['useragent']).decode('utf-8')
                            e.click_event = evento_sendgrid
                            e.click_email = str(body['email']).decode('utf-8')
                            e.click_date = body['timestamp']
                            e.click_url = str(body['url']).decode('utf-8')
                            e.save()
                            # proceso intermedio de soap web service
                            soap_ws = SoapMiddleware(e.pk, evento_sendgrid)
                            soap_ws.evaluate()
                            # proceso de registrar eventos en tabla log
                            EmailLogEvent.write_event(evento_sendgrid, body)
                else:
                    logger.error("parametros incompletos, correo no corresponde.")
            except Exception, e:
                logger.error(e)
                return HttpResponse(e, status=500)
        return HttpResponse()
