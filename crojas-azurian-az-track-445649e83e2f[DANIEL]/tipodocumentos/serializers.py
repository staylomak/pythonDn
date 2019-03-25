# -*- coding: utf-8 -*-


from rest_framework.serializers import ModelSerializer


from .models import TipoDocumento


class TipoDocumentoSerializer(ModelSerializer):

    class Meta:
        model = TipoDocumento
        fields = ('id_documento', 'nombre_documento', 'es_electronico',)
