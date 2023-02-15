from django.db import models
from simple_history.models import HistoricalRecords

class DiscountPercent(models.Model):
    name = models.CharField(max_length=25)
    percent = models.FloatField()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Discount percent"
        verbose_name_plural = "Discount percents"

class Orders(models.Model):
    number = models.IntegerField(unique=True)
    date = models.DateTimeField(auto_now_add=True)
    sum = models.IntegerField()
    percent = models.IntegerField()
    discount_amount = models.IntegerField()

    def __str__(self):
        return f'order {self.number}'

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

class Goods(models.Model):
    order = models.ManyToManyField(Orders)
    name = models.CharField(max_length=50)
    cost = models.FloatField()
    discount_cost = models.FloatField()

    def __str__(self):
        return {self.name}

    class Meta:
        verbose_name = "Good"
        verbose_name_plural = "Goods"


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
    history = HistoricalRecords()

    def __str__(self):
        return f'Card {self.number}'

    class Meta:
        verbose_name = "Card"
        verbose_name_plural = "Cards"

class BagCards(CardTemplate):
    history = HistoricalRecords()

    def __str__(self):
        return f'BagCard {self.number}'

    class Meta:
        verbose_name = "BagCard"
        verbose_name_plural = "BagCards"

