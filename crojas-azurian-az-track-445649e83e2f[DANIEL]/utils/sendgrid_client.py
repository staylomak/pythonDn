# -*- coding: utf-8 -*-


import base64
import logging

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from sendgrid.helpers.mail import Email
from sendgrid.helpers.mail import Personalization
from sendgrid.helpers.mail import Content
from sendgrid.helpers.mail import Attachment
from sendgrid.helpers.mail import CustomArg

from django.contrib.auth.models import User

from configuraciones.models import SendgridConf, TemplateReporte
from utils.generics import get_file_name_from_storage

logger = logging.getLogger("utils")


class EmailClient(object):
    def __init__(self, empresa_id):
        try:
            self.empresa_id = empresa_id
            # llamar las configuraciones en la DB
            self.email_config = SendgridConf.get_sg_config(self.empresa_id)
            # crear los atributos de la instancia de SendGrid
            self.sg = SendGridAPIClient(api_key=self.email_config.api_key)
            # build message
            self.message = Mail()
            self.message.from_email = Email(self.email_config.asunto_email_dte,
                                            self.email_config.nombre_email_dte)
            # set personalization
            self.personalization = Personalization()
            logger.info("Se instanció EmailClient para la empresa : " + empresa_id)
        except Exception as e:
            logger.error("Error al instanciar EmailClient")
            logger.error(e)
            raise Exception(e)

    def enviar_correo_dte(self, correo):
        try:
            # valores de envío
            self.personalization.add_to(Email(correo.correo, correo.nombre_cliente))
            self.message.subject = correo.asunto
            self.message.add_content(Content("text/html", correo.html))
            # valores personalizados
            self.personalization.add_custom_arg(CustomArg('email_id', str(correo.id)))
            self.personalization.add_custom_arg(CustomArg('empresa', correo.empresa.rut))
            self.personalization.add_custom_arg(CustomArg('rut_receptor', correo.rut_receptor))
            self.personalization.add_custom_arg(CustomArg('rut_emisor', correo.rut_emisor))
            self.personalization.add_custom_arg(CustomArg('tipo_envio', correo.tipo_envio))
            self.personalization.add_custom_arg(CustomArg('tipo_dte', str(correo.tipo_dte.id_documento)))
            self.personalization.add_custom_arg(CustomArg('numero_folio', str(correo.numero_folio)))
            self.personalization.add_custom_arg(CustomArg('resolucion_receptor', str(correo.resolucion_receptor)))
            self.personalization.add_custom_arg(CustomArg('resolucion_emisor', str(correo.resolucion_emisor)))
            self.personalization.add_custom_arg(CustomArg('monto', str(correo.monto)))
            self.personalization.add_custom_arg(CustomArg('fecha_emision', str(correo.fecha_emision)))
            self.personalization.add_custom_arg(CustomArg('fecha_recepcion', str(correo.fecha_recepcion)))
            self.personalization.add_custom_arg(CustomArg('estado_documento', correo.estado_documento))
            self.personalization.add_custom_arg(CustomArg('tipo_operacion', correo.tipo_operacion))
            self.personalization.add_custom_arg(CustomArg('tipo_receptor', correo.tipo_receptor))
            self.personalization.add_custom_arg(CustomArg('id_envio', str(correo.id_envio)))

            logger.info(correo)

            if correo.xml:
                attach = Attachment()
                attach.filename = get_file_name_from_storage(correo.xml.name)
                attach.content = base64.b64encode(correo.xml.file.read())
                self.message.add_attachment(attach)
            if correo.pdf:
                attach = Attachment()
                attach.filename = get_file_name_from_storage(correo.pdf.name)
                attach.content = base64.b64encode(correo.pdf.file.read())
                self.message.add_attachment(attach)
            if correo.adjunto1:
                attach = Attachment()
                attach.filename = get_file_name_from_storage(correo.adjunto1.name)
                attach.content = base64.b64encode(correo.adjunto1.file.read())
                self.message.add_attachment(attach)
            self.message.add_personalization(self.personalization)
            # enviando el mail
            response = self.sg.client.mail.send.post(request_body=self.message.get())
            # imprimiendo respuesta
            logger.info(response.status_code)
            logger.info(response.headers)
            logger.info(response.body)
        except Exception as e:
            logger.error("Error EmailClient.enviar_correo_dte ")
            logger.error(e)
            raise Exception(e)

    def send_report_to_user_with_attach(self, user_email, report):
        try:
            # parametros de correo reporte
            self.message.from_email = Email(self.email_config.asunto_email_reporte,
                                            self.email_config.nombre_email_reporte)
            # buscar usuario
            template_config = TemplateReporte.get_configuration(self.empresa_id)
            # preparar template del correo reporte
            user = User.objects.get(email=user_email)
            html = str(template_config.template_html).format(user_name=user.first_name)
            # valores de envío
            self.personalization.add_to(Email(user_email, user.first_name))
            self.message.subject = template_config.asunto_reporte
            self.message.add_content(Content("text/html", html))
            # adjuntar excel si esta
            if report['report']:
                attach = Attachment()
                attach.content = base64.b64encode(report['report'])
                attach.filename = report['name']
                self.message.add_attachment(attach)
            self.message.add_personalization(self.personalization)
            # enviando el correo
            response = self.sg.client.mail.send.post(request_body=self.message.get())
            # imprimiendo respuesta
            logger.info(response)
            logger.info(response.status_code)
            logger.info(response.headers)
            logger.info(response.body)
        except Exception as e:
            logger.error("Error en EmailClient.send_report_to_user_with_attach")
            logger.error(e)
            raise Exception(e)
