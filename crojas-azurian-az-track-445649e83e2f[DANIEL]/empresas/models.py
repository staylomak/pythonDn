# -*- coding: utf-8 -*-


from __future__ import unicode_literals


from django.db import models
from django.shortcuts import get_object_or_404


class Holding(models.Model):
    """ Modelo que representa a un cliente Azurian Track,
        el cual podrá tener muchas empresas asociadas.
    """

    nombre = models.CharField(max_length=200, unique=True, db_index=True)

    class Meta:
        ordering = ['nombre',]

    def __unicode__(self):
        return u'{0}'.format(self.nombre)


class Empresa(models.Model):
    """ Modelo que representa a una empresa de un cliente o Holding,
        que permitirá aislar los datos.
    """

    holding = models.ForeignKey(Holding)
    rut = models.CharField(primary_key=True, unique=True, max_length=20)
    empresa = models.CharField(max_length=200)

    class Meta:
        ordering = ['holding', 'empresa',]

    def __unicode__(self):
        return u'{0} - {1}'.format(self.rut, self.empresa)


class CamposOpcionalesEmail(models.Model):
    empresa = models.OneToOneField(Empresa)
    opcional1 = models.CharField(max_length=120, db_index=True)
    opcional2 = models.CharField(max_length=120, db_index=True, null=True, blank=True)
    opcional3 = models.CharField(max_length=120, db_index=True, null=True, blank=True)

    class Meta:
        ordering = ['empresa']

    def __unicode__(self):
        return u'{0}: {1} - {2} - {3}'.format(
            self.empresa, self.opcional1, self.opcional2, self.opcional3)

    @classmethod
    def get_campos(self, rut_empresa):
        return get_object_or_404(CamposOpcionalesEmail, empresa_id=rut_empresa)

    @classmethod
    def get_fields_to_dict(self, rut_empresa):
        try:
            campos = CamposOpcionalesEmail.objects.get(empresa_id=rut_empresa)
            if campos is not None:
                return campos.__dict__
            else:
                return None
        except CamposOpcionalesEmail.DoesNotExist:
            return None
