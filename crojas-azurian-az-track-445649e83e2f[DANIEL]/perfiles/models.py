# -*- coding: utf-8 -*-


from __future__ import unicode_literals


from django.contrib.auth.models import User
from django.db import models


from empresas.models import Empresa


class Perfil(models.Model):
    usuario = models.OneToOneField(User)
    empresas = models.ManyToManyField(Empresa)
    enable_report = models.BooleanField(default=True)

    class Meta:
        ordering = ['usuario']

    def __unicode__(self):
        return u'{0}: {1}'.format(self.usuario, self.enable_report)

    @classmethod
    def get_perfil(self, user):
        try:
            return Perfil.objects.get(usuario=user)
        except Perfil.DoesNotExist:
            return None
