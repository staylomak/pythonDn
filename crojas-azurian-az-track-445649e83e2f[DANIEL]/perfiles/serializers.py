# -*- coding: utf-8 -*-


from rest_framework.serializers import ModelSerializer


from .models import Perfil
from empresas.serializers import EmpresaSerializer


class PerfilSerializer(ModelSerializer):
    empresas = EmpresaSerializer(allow_null=True, read_only=True, many=True)

    class Meta:
        model = Perfil
        fields = ('usuario', 'empresas', 'enable_report',)
