from django.urls import path
from django.contrib import admin
from .models import DiscountPercent, Orders, Goods, Card, BagCards
from django.utils.html import format_html
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect

admin.site.register(DiscountPercent)
admin.site.register(Orders)
admin.site.register(Goods)


def restore_in_cards(obj):
    percent = obj.percent.all()
    order = obj.order.all()
    card = Card.objects.create(
        series=obj.series,
        number=obj.number,
        created_at=obj.created_at,
        date_end=obj.date_end,
        latest_use=obj.latest_use,
        summa_purchases=obj.summa_purchases,
        status=obj.status,
    )
    for obj_percent in percent:
        card.percent.add(obj_percent)
    for obj_order in order:
        card.order.add(obj_order)
    card.save()
    obj.delete()


@admin.register(BagCards)
class BagCardsAdmin(admin.ModelAdmin):
    list_display = (
        'series',
        'number',
        'created_at',
        'date_end',
        'status',
    )
    list_filter = (
        'series',
        'number',
        'created_at',
        'date_end',
        'status',
    )
    search_fields = ('series', 'number')
    actions = ['restore_actions']
    change_form_template = "admin/cards/my_change_form.html"

    def restore_actions(self, form, queryset):
        for obj in queryset:
            restore_in_cards(obj)
        return format_html(
            '<a class="button" href="{}">Restore</a>',
            reverse('admin:cards_card_changelist'),
        )

    restore_actions.short_description = 'Restore record'
    restore_actions.allow_tags = True

    def response_change(self, request, obj):
        if "restore" in request.POST:
            restore_in_cards(obj)
            self.message_user(request, "Restoring complete")
            return HttpResponseRedirect("/admin/cards/card/")
        return super().response_change(request, obj)


def add_in_bag(obj):
    percent = obj.percent.all()
    order = obj.order.all()
    bag = BagCards.objects.create(
        series=obj.series,
        number=obj.number,
        created_at=obj.created_at,
        date_end=obj.date_end,
        latest_use=obj.latest_use,
        summa_purchases=obj.summa_purchases,
        status=obj.status,
    )
    for obj_percent in percent:
        bag.percent.add(obj_percent)
    for obj_order in order:
        bag.order.add(obj_order)
    bag.save()


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = (
        'series',
        'number',
        'created_at',
        'date_end',
        'status',
    )
    list_filter = (
        'series',
        'number',
        'created_at',
        'date_end',
        'status',
    )
    search_fields = ('series', 'number')

    def delete_model(self, form, change):
        add_in_bag(change)
        print(BagCards.objects.all())
        super().delete_model(form, change)

    def delete_queryset(self, form, queryset):
        print(queryset)
        for obj in queryset:
            add_in_bag(obj)
        super().delete_queryset(form, queryset)

