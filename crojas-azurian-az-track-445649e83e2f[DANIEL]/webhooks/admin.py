# -*- coding: utf-8 -*-


from django.contrib import admin


from .models import EmailLogEvent


class EmailLogEventAdmin(admin.ModelAdmin):
    list_display = ('input_date', 'correo', 'numero_folio',
                    'tipo_dte', 'fecha_evento', 'nombre_evento')


admin.site.register(EmailLogEvent, EmailLogEventAdmin)
