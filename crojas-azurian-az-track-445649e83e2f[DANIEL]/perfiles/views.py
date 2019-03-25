# -*- coding: utf-8 -*-


from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import Perfil
from .serializers import PerfilSerializer


class PerfilesView(APIView):
    serializer_class = PerfilSerializer
    permission_classes = (permissions.IsAuthenticated,)

    # Retorna un perfil en base a un nombre de usuario
    def get(self, request, *args, **kwargs):
        try:
            if request.user is not None:
                perfil = Perfil.get_perfil(request.user)
                response = self.serializer_class(perfil, many=False)
                return Response(response.data)
        except Perfil.DoesNotExist:
            return Response({"Usuario no existe"},
                            status=status.HTTP_404_NOT_FOUND)
