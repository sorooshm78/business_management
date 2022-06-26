from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Repository(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    amount = models.IntegerField(default=0)

    def add_price(self, price):
        self.amount += price
        self.save()

    def sub_price(self, price):
        self.amount -= price
        self.save()

    @staticmethod
    def get_sum_amount(user_id):
        sum_amount = 0
        for repo in Repository.objects.filter(user_id=user_id).all():
            sum_amount += repo.amount
        return sum_amount

    def __str__(self):
        return self.name
