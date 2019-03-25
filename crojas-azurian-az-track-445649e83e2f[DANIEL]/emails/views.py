# -*- coding: utf-8 -*-


import logging


from django.http import HttpResponse
from django.views.generic import TemplateView


from rest_framework import authentication, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import Email
from .serializers import EmailDteInputSerializer, EmailTrackDTESerializer
from .tasks import input_queue, send_emails_no_delivered
from utils.generics import to_unix_timestamp
from utils.sendgrid_client import EmailClient


logger = logging.getLogger(__name__)


class EmailDteInputView(APIView):
    """ Vista encargada de recibir los request vía post para crear nuevos email
        y enviarlos por correo utilizando SendGrid
    """
    # authentication_classes = (authentication.TokenAuthentication,)
    serializer_class = EmailDteInputSerializer
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        # Método que permite consultar el estado de un correo.
        logger.info(request.query_params)
        query_params = request.query_params
        params = dict()

        try:
            # Validar si vienen parametros en el GET
            params['correo'] = query_params['correo']
            params['numero_folio'] = query_params['numero_folio']
            params['tipo_dte'] = query_params['tipo_dte']
            params['rut_emisor'] = query_params['rut_emisor']
            params['resolucion_emisor'] = query_params['resolucion_emisor']
            params['id_envio'] = query_params['id_envio']
            try:
                params['tipo_receptor'] = query_params['tipo_receptor']
            except:
                params['tipo_receptor'] = None

            # imprimiendo parametros
            logger.info(params)
            # consulta
            email = Email.get_email(**params)
            # imprimir resultado de la consulta
            logger.info(email)
            if email is not None:
                logger.info("no es vacío")
                # serializar
                response = EmailTrackDTESerializer(email, many=False)
                # responder
                return Response(response.data)
            else:
                logger.info("es vacío")
                return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception, e:
            return Response({"mensaje": "Error en parametros enviados."})

    def post(self, request, format=None):
        """ Método que permite el input de un correo para ser
            gestionado por el Track.
        """
        # guardar el request data
        data = request.data
        # validar que el formato fecha sea de largo 10
        data['fecha_emision'] = to_unix_timestamp(data['fecha_emision'])
        data['fecha_recepcion'] = to_unix_timestamp(data['fecha_emision'])
        email = EmailDteInputSerializer(data=data)

        if email.is_valid():
            try:
                email.save()
                logger.info(email.data)
                correo = Email.objects.get(pk=email.data['id'])
                input_queue(correo)
                return Response({'status': 200})
            except Exception as e:
                logger.error("Error al guardar email")
                logger.error(e)
                return Response({'status': 500})
        else:
            logger.error(email.errors)
            return Response(email.errors)


class SendDelayedEmails(TemplateView):

    def get(self, request, rut_empresa, *args, **kwargs):
        if rut_empresa:
            logger.info("Rut empresa")
            rut_empresa = str(rut_empresa)
        emails = Email.get_emails_no_delivered(rut_empresa)
        if emails.count() > 0:
            logger.info("Se encontraron {0} correos.".format(emails.count()))
            for email in emails:
                email_client = EmailClient(email.empresa_id)
                email_client.enviar_correo_dte(email)
            return HttpResponse("Se encontraron {0} correos.".format(emails.count()))
        else:
            logger.info("No se encontraron correos")
            return HttpResponse("No se encontraron correos.")
