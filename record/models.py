from django.db import models

from repository.models import Repository

# class RecordType(TextChoices):
#     input = 'input', 'دریافتی'
#     output = 'output', 'مخارج'
#
#
# class PaymentType(TextChoices):
#     cash = 'cash', 'نقدی'
#     cart = 'cart', 'کارت'

RecordType = [
    ('input', 'دریافتی'),
    ('output', 'مخارج'),
]
PaymentType = [
    ('cash', 'نقدی'),
    ('cart', 'کارت'),
]


class Record(models.Model):
    repository = models.ForeignKey(to=Repository, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    payment_type = models.CharField(
        max_length=30,
        choices=PaymentType,
    )
    record_type = models.CharField(
        max_length=30,
        choices=RecordType,
    )

    category = models.ForeignKey(to='category.Category', on_delete=models.CASCADE, null=True, blank=True)
    price = models.IntegerField()
    date = models.CharField(max_length=40)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
