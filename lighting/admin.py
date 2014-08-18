from django.contrib import admin

import models


#class UnitAdmin(admin.ModelAdmin):
#    list_display = ('name', 'dir_name', 'is_active')
#    list_filter = ('form_class', )
#    search_fields = ('name', )
#    fields = ('name', 'dir_name', 'desc', 'form_class', 'is_active')
#
#
#admin.site.register(models.Unit, UnitAdmin)

admin.site.register(models.Unit)