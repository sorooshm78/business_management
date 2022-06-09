from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Repository(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    cash = models.IntegerField(default=0)
    cart = models.IntegerField(default=0)

    def get_total_value(self):
        return self.cart + self.cash

    @staticmethod
    def get_sum_cart(user_id):
        sum_cart = 0
        for repo in Repository.objects.filter(user_id=user_id).all():
            sum_cart += repo.cart
        return sum_cart

    @staticmethod
    def get_sum_cash(user_id):
        sum_cash = 0
        for repo in Repository.objects.filter(user_id=user_id).all():
            sum_cash += repo.cash
        return sum_cash

    def __str__(self):
        return self.name


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


class Category(models.Model):
    name = models.CharField(max_length=30)
    record_type = models.CharField(
        max_length=30,
        choices=RecordType,
    )

    def __str__(self):
        return self.name


class Record(models.Model):
    repository = models.ForeignKey(to=Repository, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    payment_type = models.CharField(
        max_length=30,
        choices=PaymentType,
    )
    record_type = models.CharField(
        max_length=30,
        choices=RecordType,
    )

    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    date = models.DateField()
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
