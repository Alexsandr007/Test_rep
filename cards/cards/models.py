from django.db import models


class DiscountPercent(models.Model):
    name = models.CharField(max_length=25)
    percent = models.FloatField()


class Orders(models.Model):
    number = models.IntegerField(unique=True)
    date = models.DateTimeField(auto_now_add=True)
    sum = models.IntegerField()
    percent = models.IntegerField()
    discount_amount = models.IntegerField()


class Goods(models.Model):
    order = models.ManyToManyField(Orders)
    name = models.CharField(max_length=50)
    cost = models.FloatField()
    discount_cost = models.FloatField()


class Status(models.TextChoices):
    active = 'Active'
    inactive = 'Inactive'
    frozen = 'Frozen'

class CardTemplate(models.Model):
    series = models.IntegerField()
    number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    date_end = models.DateTimeField()
    latest_use = models.DateTimeField(auto_now=True)
    summa_purchases = models.IntegerField()
    status = models.CharField(
        max_length=25,
        choices=Status.choices,
        default=Status.active
    )
    percent = models.ManyToManyField(DiscountPercent)
    order = models.ManyToManyField(Orders)

    class Meta:
        abstract = True


class Card(CardTemplate):

    def __str__(self):
        return f'Card {self.number}'


class BagCards(CardTemplate):

    def __str__(self):
        return f'BagCard {self.number}'

