from django.contrib import admin
from .models import DiscountPercent, Orders, Goods, Card, BagCards

admin.site.register(DiscountPercent)
admin.site.register(Orders)
admin.site.register(Goods)
admin.site.register(BagCards)


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):

    def delete_model(self, form, change):
        percent = change.percent.all()
        order = change.order.all()
        bag = BagCards.objects.create(
            series=change.series,
            number=change.number,
            created_at=change.created_at,
            date_end=change.date_end,
            latest_use=change.latest_use,
            summa_purchases=change.summa_purchases,
            status=change.status,
        )
        for obj in percent:
            bag.percent.add(obj)
        for obj in order:
            bag.order.add(obj)
        bag.save()
        super().delete_model(form, change)
