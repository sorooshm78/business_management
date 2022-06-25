from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Repository(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    cash = models.IntegerField(default=0)
    cart = models.IntegerField(default=0)

    def add_price(self, payment_type, price):
        if payment_type == 'cart':
            self.cart += int(price)
        elif payment_type == 'cash':
            self.cash += int(price)
        self.save()

    def sub_price(self, payment_type, price):
        if payment_type == 'cart':
            self.cart -= int(price)
        elif payment_type == 'cash':
            self.cash -= int(price)
        self.save()

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
