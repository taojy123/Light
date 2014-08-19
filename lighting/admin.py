from django.contrib import admin

import models


class UnitAdmin(admin.ModelAdmin):
    list_display = ('anum', 'rnum', 'name', 'project_name')
    search_fields = ('name', )



admin.site.register(models.Unit, UnitAdmin)

#admin.site.register(models.Unit)