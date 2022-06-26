from django.contrib import admin

# Register your models here.
from repository import models


class RepositoryAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'name',
    ]


admin.site.register(models.Repository, RepositoryAdmin)
