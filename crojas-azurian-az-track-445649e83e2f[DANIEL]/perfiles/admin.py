# -*- coding: utf-8 -*-


from django.contrib import admin


from .models import Perfil


class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'enable_report',)
    list_filter = ('empresas__holding', 'empresas', 'usuario',)
    ordering = ('usuario',)


admin.site.register(Perfil, PerfilAdmin)
