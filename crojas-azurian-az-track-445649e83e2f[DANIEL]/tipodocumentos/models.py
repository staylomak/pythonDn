# -*- coding: utf-8 -*-


from __future__ import unicode_literals


from django.db import models


class TipoDocumento(models.Model):
    id_documento = models.IntegerField(primary_key=True, unique=True)
    nombre_documento = models.CharField(max_length=200)
    es_electronico = models.BooleanField()

    class Meta:
        ordering = ['id_documento']

    def __unicode__(self):
        return self.nombre_documento
