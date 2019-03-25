# -*- coding: utf-8 -*-


from django.contrib import admin


from .models import Email


class EmailAdmin(admin.ModelAdmin):
    list_display = ('input_date', 'correo', 'rut_emisor', 'numero_folio', 'empresa',)
    list_filter = ('input_date', 'rut_emisor', 'empresa',)
    search_fields = ('input_date', 'correo', 'rut_emisor', 'numero_folio', 'empresa',)


admin.site.register(Email, EmailAdmin)
