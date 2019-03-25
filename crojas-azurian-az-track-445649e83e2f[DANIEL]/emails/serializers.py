# -*- coding: utf-8 -*-


from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import FileField
from rest_framework.serializers import IntegerField
from rest_framework.serializers import CharField


from .models import Email
from empresas.serializers import EmpresaSerializer
from tipodocumentos.serializers import TipoDocumentoSerializer


class EmailDteInputSerializer(ModelSerializer):
    """
    Serializador del input de correos desde el DTE.
    Agregando el serializador de empresa anida la relación
    en el json de listado del modelo emails, pero en los
    parámetros rest hay que enviarlos.
    """
    xml = FileField(use_url=False, max_length=None, allow_null=True,
                    allow_empty_file=True, required=False)
    pdf = FileField(use_url=False, max_length=None, allow_null=True,
                    allow_empty_file=True, required=False)
    adjunto1 = FileField(use_url=False, max_length=None, allow_null=True,
                         allow_empty_file=True, required=False)
    opcional1 = CharField(allow_null=True, required=False)
    opcional2 = CharField(allow_null=True, required=False)
    opcional3 = CharField(allow_null=True, required=False)

    class Meta:
        model = Email
        fields = (
            'id', 'input_date', 'empresa', 'rut_receptor', 'rut_emisor',
            'tipo_envio', 'tipo_dte', 'numero_folio', 'resolucion_receptor',
            'resolucion_emisor', 'monto', 'fecha_emision', 'fecha_recepcion',
            'estado_documento', 'id_envio', 'tipo_operacion', 'tipo_receptor',
            'nombre_cliente', 'correo', 'asunto', 'html', 'xml', 'pdf',
            'adjunto1', 'opcional1', 'opcional2', 'opcional3'
        )


class EmailTrackDTESerializer(ModelSerializer):
    """
    Serializador del objeto de respuesta a las consultas de la traza
    de los correos realizadas desde el DTE.
    """
    xml = FileField(use_url=False, max_length=None, allow_null=True,
                    allow_empty_file=True, required=False)
    pdf = FileField(use_url=False, max_length=None, allow_null=True,
                    allow_empty_file=True, required=False)
    adjunto1 = FileField(use_url=False, max_length=None, allow_null=True,
                         allow_empty_file=True, required=False)
    resolucion_receptor = IntegerField(allow_null=True, required=False)
    fecha_recepcion = IntegerField(allow_null=True, required=False)
    opcional1 = CharField(allow_null=True, required=False)
    opcional2 = CharField(allow_null=True, required=False)
    opcional3 = CharField(allow_null=True, required=False)

    class Meta:
        model = Email
        fields = (
            'id', 'input_date', 'empresa', 'rut_receptor', 'rut_emisor',
            'tipo_envio', 'tipo_dte', 'numero_folio', 'resolucion_receptor',
            'resolucion_emisor', 'monto', 'fecha_emision', 'fecha_recepcion',
            'estado_documento', 'id_envio', 'tipo_operacion', 'tipo_receptor',
            'nombre_cliente', 'correo', 'asunto', 'xml', 'pdf', 'adjunto1',
            'opcional1', 'opcional2', 'opcional3',
            'processed_date', 'processed_event',
            'delivered_date', 'delivered_event', 'delivered_response',
            'opened_first_date', 'opened_last_date', 'opened_event',
            'opened_ip', 'opened_user_agent', 'opened_count',
            'dropped_date', 'dropped_reason', 'dropped_event',
            'bounce_date', 'bounce_event', 'bounce_reason', 'bounce_status', 'bounce_type',
            'unsubscribe_date', 'unsubscribe_purchase', 'unsubscribe_event',
            'click_ip', 'click_purchase', 'click_useragent', 'click_event',
            'click_email', 'click_date', 'click_url',
        )


class EmailTrackRelatedSerializer(ModelSerializer):
    """ Serializa los correos para poder ser desplegados en la tabla
        del menú customsearch o detalle de email.
    """
    tipo_dte = TipoDocumentoSerializer(many=False, read_only=True)
    empresa = EmpresaSerializer(many=False, read_only=True)
    xml = FileField(use_url=False, max_length=None, allow_null=True,
                    allow_empty_file=True, required=False)
    pdf = FileField(use_url=False, max_length=None, allow_null=True,
                    allow_empty_file=True, required=False)
    adjunto1 = FileField(use_url=False, max_length=None, allow_null=True,
                         allow_empty_file=True, required=False)
    resolucion_receptor = IntegerField(allow_null=True, required=False)
    fecha_recepcion = IntegerField(allow_null=True, required=False)
    opcional1 = CharField(allow_null=True, required=False)
    opcional2 = CharField(allow_null=True, required=False)
    opcional3 = CharField(allow_null=True, required=False)

    class Meta:
        model = Email
        fields = (
            'id', 'input_date', 'empresa', 'rut_receptor', 'rut_emisor',
            'tipo_envio', 'tipo_dte', 'numero_folio', 'resolucion_receptor',
            'resolucion_emisor', 'monto', 'fecha_emision', 'fecha_recepcion',
            'estado_documento', 'id_envio', 'tipo_operacion', 'tipo_receptor',
            'nombre_cliente', 'correo', 'asunto', 'xml', 'pdf', 'adjunto1',
            'opcional1', 'opcional2', 'opcional3',
            'processed_date', 'processed_event',
            'delivered_date', 'delivered_event', 'delivered_response',
            'opened_first_date', 'opened_last_date', 'opened_event',
            'opened_ip', 'opened_user_agent', 'opened_count',
            'dropped_date', 'dropped_reason', 'dropped_event',
            'bounce_date', 'bounce_event', 'bounce_reason', 'bounce_status', 'bounce_type',
            'unsubscribe_date', 'unsubscribe_purchase', 'unsubscribe_event',
            'click_ip', 'click_purchase', 'click_useragent', 'click_event',
            'click_email', 'click_date', 'click_url',
        )
