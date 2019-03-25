# -*- coding: utf-8 -*-


from __future__ import unicode_literals


from django.db import models


class Report(models.Model):
    input_date = models.DateField(auto_now_add=True, db_index=True)
    name = models.CharField(max_length=120)
    report = models.FileField(upload_to='reportes/%Y/%m/%d/%H%M%S')

    def __unicode__(self):
        return self.name
