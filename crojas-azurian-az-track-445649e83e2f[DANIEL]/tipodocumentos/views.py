# -*- coding: utf-8 -*-


from rest_framework.viewsets import ModelViewSet


from .models import TipoDocumento
from .serializers import TipoDocumentoSerializer


class TipoDocumentoViewSet(ModelViewSet):
    model = TipoDocumento
    queryset = TipoDocumento.objects.all()
    serializer_class = TipoDocumentoSerializer
