# -*- coding: utf-8 -*-


from rest_framework.serializers import ModelSerializer


from .models import CamposOpcionalesEmail, Empresa, Holding


class HoldingSerializer(ModelSerializer):

    class Meta:
        model = Holding
        fields = ('nombre',)


class EmpresaSerializer(ModelSerializer):

    holding = HoldingSerializer(many=False, read_only=True)

    class Meta:
        model = Empresa
        fields = ('rut', 'empresa', 'holding')


class CamposOpcionalesEmailSerializer(ModelSerializer):

    class Meta:
        model = CamposOpcionalesEmail
        fields = ('empresa', 'opcional1', 'opcional2', 'opcional3',)
