# Create your models here.
from django.db import models

# import record.models
from record.models import RecordType
from repository.models import Repository


class Category(models.Model):
    repository = models.ForeignKey(to=Repository, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    record_type = models.CharField(
        max_length=30,
        choices=RecordType,
    )

    def __str__(self):
        return self.name
