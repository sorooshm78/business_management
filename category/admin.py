from django.contrib import admin

# Register your models here.
from category import models


class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'record_type',
    ]


admin.site.register(models.Category, CategoryAdmin)
