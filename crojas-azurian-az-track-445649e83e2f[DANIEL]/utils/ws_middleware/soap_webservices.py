# -*- coding: utf-8 -*-

""" Middleware para la manipulacion de eventos SendGrid
    para enviarlo a un WebService definido por el cliente
    al que se le implementa el DTE Tracking.

    Pasos:
        1.- Validar si existe una URL del WebService,
        2.-
"""


from datetime import datetime
import logging
from suds.client import Client


from configuraciones.models import SoapWebService
from emails.models import Email
from utils.generics import timestamp_to_date
from webhooks.tasks import soap_ws_task


logger = logging.getLogger(__name__)


class SoapMiddleware(object):

    def __init__(self, email_id, event):
        self.email_id = email_id
        self.event = event
        holding = Email.get_email_by_id(email_id).empresa.holding
        self.soap_conf = SoapWebService.get_ws_conf(holding)
        logger.info("Objeto SoapMiddleware creado")

    def evaluate(self):
        if self.soap_conf is not None:
            context = {
                'email_id': self.email_id,
                'event': self.event,
            }
            logger.info(
                'Email id {0} paso a cola de SoapWS'.format(self.email_id))
            soap_ws_task(context)
        else:
            logger.info('Email no tiene conf de SoapWS')

    def execute(self):
        """ Validar si la URL para el servicio web esta
            disponible
        """
        if self.soap_conf.url:
            # Creacion de la instancia Client
            client = Client(self.soap_conf.url, cache=None)
            email = Email.get_email_by_id(self.email_id)
            documento = None
            body = None

            if email is not None:
                email = email.__dict__

                if self.soap_conf.con_autenticacion:
                    """ Método por definir cuando el cliente solicita
                        algún metodo de autenticación a un web service
                    """
                    pass

                if self.soap_conf.con_objeto_documento:
                    # Se prepara el objeto documento
                    logger.info("creando objeto documento")
                    documento = client.factory.create(
                        self.soap_conf.nombre_objeto_documento)
                    doc_attr = self.soap_conf.parametros_objeto_documento.split(';')
                    doc_field = self.soap_conf.campos_objeto_documento.split(';')

                    for att, field in map(None, doc_attr, doc_field):
                        documento[att] = email[field]

                    logger.info("imprimiendo documento")
                    logger.info(documento)

                if self.soap_conf.con_objeto_request:
                    logger.info("Creando objeto request")
                    body = client.factory.create(self.soap_conf.nombre_objeto_request)

                if self.soap_conf.solo_default:
                    """ Método por definir cuando se utiliza un solo metodo para
                        notificar eventos sendgrid a un web service
                    """
                    pass
                else:

                    if self.event == 'processed':
                        logger.info("ws procesados")
                        data = dict()
                        params = self.soap_conf.parametros_procesado.split(';')
                        fields = self.soap_conf.campos_procesado.split(';')

                        client = getattr(client.service, self.soap_conf.metodo_procesado)

                        for param, field in map(None, params, fields):
                            logger.info(field)
                            logger.info(email[field])

                            """ Validar si los parametros se guardan en
                                la variable data o en body.
                            """
                            if self.soap_conf.con_objeto_request:

                                if field.endswith('_date') and email[field] is not None:
                                    logger.info(email[field])
                                    field = timestamp_to_date(email[field])
                                    body[param] = field

                                elif field.endswith('_date') and email[field] is None:
                                    body[param] = datetime.now()

                                else:
                                    body[param] = email[field]

                                if documento is not None:
                                    body[self.soap_conf.nombre_parametro_documento] = documento

                                logger.info("imprimiendo resultado del WS")
                                logger.info(client(body))

                            else:

                                if field.endswith('_date') and email[field] is not None:
                                    logger.info(email[field])
                                    field = timestamp_to_date(email[field])
                                    data[param] = field

                                elif field.endswith('_date') and email[field] is None:
                                    data[param] = datetime.now()

                                else:
                                    data[param] = email[field]

                                if documento is not None:
                                    data[self.soap_conf.nombre_parametro_documento] = documento

                                logger.info("imprimiendo resultado del WS")
                                logger.info(client(**data))

                    elif self.event == 'delivered':
                        logger.info("ws enviados")
                        data = dict()
                        params = self.soap_conf.parametros_enviado.split(';')
                        fields = self.soap_conf.campos_enviado.split(';')

                        client = getattr(client.service, self.soap_conf.metodo_enviado)

                        for param, field in map(None, params, fields):
                            logger.info(field)

                            if self.soap_conf.con_objeto_request:

                                if field.endswith('_date') and email[field] is not None:
                                    logger.info(email[field])
                                    field = timestamp_to_date(email[field])
                                    body[param] = field

                                elif field.endswith('_date') and email[field] is None:
                                    body[param] = datetime.now()

                                else:
                                    body[param] = email[field]

                                if documento is not None:
                                    body[self.soap_conf.nombre_parametro_documento] = documento

                                logger.info("imprimiendo resultado del WS")
                                logger.info(client(body))

                            else:

                                if field.endswith('_date') and email[field] is not None:
                                    logger.info(email[field])
                                    field = timestamp_to_date(email[field])
                                    data[param] = field

                                elif field.endswith('_date') and email[field] is None:
                                    data[param] = datetime.now()

                                else:
                                    data[param] = email[field]

                                if documento is not None:
                                    data[self.soap_conf.nombre_parametro_documento] = documento

                                logger.info("imprimiendo resultado del WS")
                                logger.info(client(**data))

                    elif self.event == 'open':
                        logger.info("ws leidos")
                        data = dict()
                        params = self.soap_conf.parametros_leido.split(';')
                        fields = self.soap_conf.campos_leido.split(';')

                        client = getattr(client.service, self.soap_conf.metodo_leido)

                        for param, field in map(None, params, fields):

                            if self.soap_conf.con_objeto_request:

                                if field.endswith('_date') and email[field] is not None:
                                    logger.info(email[field])
                                    field = timestamp_to_date(email[field])
                                    body[param] = field

                                elif field.endswith('_date') and email[field] is None:
                                    body[param] = datetime.now()

                                else:
                                    body[param] = email[field]

                                if documento is not None:
                                    body[self.soap_conf.nombre_parametro_documento] = documento

                                logger.info("imprimiendo resultado del WS")
                                logger.info(client(body))

                            else:

                                if field.endswith('_date') and email[field] is not None:
                                    logger.info(email[field])
                                    field = timestamp_to_date(email[field])
                                    data[param] = field

                                elif field.endswith('_date') and email[field] is None:
                                    data[param] = datetime.now()

                                else:
                                    data[param] = email[field]

                                if documento is not None:
                                    data[self.soap_conf.nombre_parametro_documento] = documento

                                logger.info("imprimiendo resultado del WS")
                                logger.info(client(**data))

                    elif self.event == 'dropped':
                        logger.info("ws rechazados")
                        data = dict()
                        params = self.soap_conf.parametros_rechazado.split(';')
                        fields = self.soap_conf.campos_rechazado.split(';')

                        client = getattr(client.service, self.soap_conf.metodo_rechazado)

                        for param, field in map(None, params, fields):

                            if self.soap_conf.con_objeto_request:

                                if field.endswith('_date') and email[field] is not None:
                                    logger.info(email[field])
                                    field = timestamp_to_date(email[field])
                                    body[param] = field

                                elif field.endswith('_date') and email[field] is None:
                                    body[param] = datetime.now()

                                else:
                                    body[param] = email[field]

                                if documento is not None:
                                    body[self.soap_conf.nombre_parametro_documento] = documento

                                logger.info("imprimiendo resultado del WS")
                                logger.info(client(body))

                            else:

                                if field.endswith('_date') and email[field] is not None:
                                    logger.info(email[field])
                                    field = timestamp_to_date(email[field])
                                    data[param] = field

                                elif field.endswith('_date') and email[field] is None:
                                    data[param] = datetime.now()

                                else:
                                    data[param] = email[field]

                                if documento is not None:
                                    data[self.soap_conf.nombre_parametro_documento] = documento

                                logger.info("imprimiendo resultado del WS")
                                logger.info(client(**data))

                    elif self.event == 'bounce':
                        logger.info("ws rebotados")
                        data = dict()
                        params = self.soap_conf.parametros_rebotado.split(';')
                        fields = self.soap_conf.campos_rebotado.split(';')

                        client = getattr(client.service, self.soap_conf.metodo_rebotado)

                        for param, field in map(None, params, fields):

                            if self.soap_conf.con_objeto_request:

                                if field.endswith('_date') and email[field] is not None:
                                    logger.info(email[field])
                                    field = timestamp_to_date(email[field])
                                    body[param] = field

                                elif field.endswith('_date') and email[field] is None:
                                    body[param] = datetime.now()

                                else:
                                    body[param] = email[field]

                                if documento is not None:
                                    body[self.soap_conf.nombre_parametro_documento] = documento

                                logger.info("imprimiendo resultado del WS")
                                logger.info(client(body))

                            else:

                                if field.endswith('_date') and email[field] is not None:
                                    logger.info(email[field])
                                    field = timestamp_to_date(email[field])
                                    data[param] = field

                                elif field.endswith('_date') and email[field] is None:
                                    data[param] = datetime.now()

                                else:
                                    data[param] = email[field]

                                if documento is not None:
                                    data[self.soap_conf.nombre_parametro_documento] = documento

                                logger.info("imprimiendo resultado del WS")
                                logger.info(client(**data))

            else:
                logger.error("Email id no corresponde")
        else:
            logger.error('No hay url soap ws configurada')
