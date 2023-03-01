import datetime

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




class Status(models.TextChoices):
    active = 'Active'
    inactive = 'Inactive'
    frozen = 'Frozen'
    overdue = 'Overdue'


def default_datetime():
    date = datetime.datetime.now()
    new_year = int(date.year) + 2
    date_end = datetime.date(new_year, date.month, date.day)
    return date_end

class CardTemplate(models.Model):
    series = models.IntegerField()
    number = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)
    date_end = models.DateField(default=default_datetime)
    latest_use = models.DateTimeField(auto_now=True)
    summa_purchases = models.IntegerField()
    status = models.CharField(
        max_length=25,
        choices=Status.choices,
        default=Status.active
    )
    percent = models.ForeignKey(DiscountPercent, on_delete=models.CASCADE)

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


class Goods(models.Model):
    name = models.CharField(max_length=50)
    cost = models.FloatField()
    discount_cost = models.FloatField()

    def __str__(self):
        return {self.name}

    class Meta:
        verbose_name = "Good"
        verbose_name_plural = "Goods"


class Orders(models.Model):
    goods = models.ManyToManyField(Goods)
    number = models.IntegerField(unique=True)
    date = models.DateTimeField(auto_now_add=True)
    sum = models.IntegerField()
    percent = models.IntegerField(null=True, blank=True)
    discount_amount = models.IntegerField(null=True, blank=True)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, null=True, blank=True, related_name='order')

    def __str__(self):
        return f'order: {self.number}| date: {self.date}| sum: {self.sum}| percent:{self.percent}| discount amount: {self.discount_amount}'

    class Meta:
        ordering = ['-date']
        verbose_name = "Order"
        verbose_name_plural = "Orders"
