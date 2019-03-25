# -*- coding: utf-8 -*-


from django.contrib import admin


from .models import Report


class ReportAdmin(admin.ModelAdmin):
    list_display = ('input_date', 'name',)
    list_filter = ('input_date', 'name',)
    search_fields = ('input_date', 'name',)


admin.site.register(Report, ReportAdmin)
