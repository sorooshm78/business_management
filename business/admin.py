from django.contrib import admin

# Register your models here.
from business import models


class RepositoryAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'name',
    ]


class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'record_type',
    ]


admin.site.register(models.Repository, RepositoryAdmin)
admin.site.register(models.Record)
admin.site.register(models.Category, CategoryAdmin)
