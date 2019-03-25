# -*- coding: utf-8 -*-


from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet


from .models import Empresa, CamposOpcionalesEmail
from .serializers import EmpresaSerializer, CamposOpcionalesEmailSerializer


class EmpresaViewSet(ModelViewSet):
    model = Empresa
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer


class CamposOpcionalesEmailView(APIView):
    serializer_class = CamposOpcionalesEmailSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, empresa, *args, **kwargs):
        empresa = str(empresa).decode('utf-8')
        campos = CamposOpcionalesEmail.get_campos(empresa)
        response = self.serializer_class(campos, many=False)
        return Response(response.data)
