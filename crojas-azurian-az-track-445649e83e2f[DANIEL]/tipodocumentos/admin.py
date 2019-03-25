# -*- coding: utf-8 -*-


from django.contrib import admin


from .models import TipoDocumento


class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = ('id_documento', 'nombre_documento', 'es_electronico',)
    list_filter = ('id_documento', 'nombre_documento', 'es_electronico',)
    search_fields = ('id_documento', 'nombre_documento', 'es_electronico',)


admin.site.register(TipoDocumento, TipoDocumentoAdmin)
