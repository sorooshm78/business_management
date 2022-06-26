from django.contrib import admin

# Register your models here.
from record import models


class RecordAdminModel(admin.ModelAdmin):
    list_display = [
        'title',
        'record_type',
        'category',
        'price',
        'date',
    ]


admin.site.register(models.Record, RecordAdminModel)