from django.shortcuts import render
from django.contrib import admin
from .models import DiscountPercent, Orders, Goods, Card, BagCards
from django.utils.html import format_html
from django.urls import reverse
from simple_history.admin import SimpleHistoryAdmin
from django.http import HttpResponseRedirect
from django.urls import path


admin.site.register(DiscountPercent)
admin.site.register(Goods)


class OrdersAdmin(admin.ModelAdmin):
    exclude = ['discount_amount', 'percent', 'bag_id']

    def save_model(self, request, obj, form, change):
        form = form.save(commit=False)
        card = form.card
        percent_models = card.percent
        percent = percent_models.percent
        form.percent = percent
        form.discount_amount = (form.sum * percent) / 100
        form.save()


admin.site.register(Orders, OrdersAdmin)


def restore_in_cards(obj):
    percent = obj.percent
    orders = Orders.objects.filter(bag_id=obj.id)
    card = Card.objects.create(
        series=obj.series,
        number=obj.number,
        created_at=obj.created_at,
        date_end=obj.date_end,
        latest_use=obj.latest_use,
        summa_purchases=obj.summa_purchases,
        status=obj.status,
        percent=percent
    )
    card.save()
    for i in orders:
        i.card = card
        i.save()
    obj.delete()


@admin.register(BagCards)
class BagCardsAdmin(SimpleHistoryAdmin):
    list_display = ('series', 'number', 'created_at', 'date_end', 'status',)
    list_filter = ('series', 'number', 'created_at', 'date_end', 'status',)
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
    percent = obj.percent
    print(percent)
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
    bag.percent = percent
    for i in obj.order.all():
        print(i)
        i.bag_id = bag.id
        i.save()
    bag.save()


class OrdersInline(admin.StackedInline):
    extra = 0
    model = Orders
    readonly_fields = ('number','goods','date','sum','percent','discount_amount')
    can_delete = False
    exclude = ['bag_id']


class WebsiteHistoryAdmin(SimpleHistoryAdmin):
    history_list_display = ('series', 'number', 'created_at', 'date_end', 'status')
    list_display = ('series', 'number','created_at', 'date_end', 'status', 'view_orders',)
    list_filter = ('series', 'number', 'created_at', 'date_end', 'status',)
    search_fields = ('series', 'number')
    actions = ['activate_status_actions', 'deactivate_status_actions']
    exclude = ['date_end']
    list_per_page = 200
    change_list_template = "admin/cards/cards_change_list.html"
    inlines = [
        OrdersInline,
    ]

    def generate_cards_form(self, request):
        return render(request, 'admin/cards/generate.html')

    def get_urls(self):
        urls = super(WebsiteHistoryAdmin, self).get_urls()
        custom_urls = [
            path('generate/form/', self.generate_cards_form, name='generate_cards_form'),
        ]
        return custom_urls + urls

    def delete_model(self, request, change):
        add_in_bag(change)
        print(BagCards.objects.all())
        super().delete_model(request, change)

    def delete_queryset(self, request, queryset):
        print(queryset)
        for obj in queryset:
            add_in_bag(obj)
        super().delete_queryset(request, queryset)

    def view_orders(self, obj):
        html = '"<table><tr><th>Number</th><th>Date</th>' \
               '<th>Sum</th><th>Percent</th><th>Discount Amount</th></tr>'
        print(obj)
        if not obj.order.all():
            html += '</table>"'
            html_end = f'<a class="button" id="button_table" onclick="func_{obj.id}({obj.id})">View table</a>' \
                       f'<div id="table_{obj.id}"></div>' \
                       '<script>' \
                       'var count = 0;' \
                       f'function func_{obj.id}(id) ' \
                       '{{{{' \
                       f'var elem = document.getElementById("table_"+String(id));' \
                       'if(count === 0) {{{{elem.innerHTML = {0};count++;}}}}' \
                       'else {{{{elem.innerHTML = "";count--}}}}' \
                       '}}}}' \
                       '</script>'.format(html)
            return format_html(html_end)
        else:
            for i in obj.order.all():
                html_columns = '<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td></tr>'.format(
                    i.number,
                    i.date.strftime("%m/%d/%Y, %H:%M:%S"),
                    i.sum,
                    i.percent,
                    i.discount_amount
                )
                html += html_columns
            html += '</table>"'

            html_end = f'<a class="button" id="button_table" onclick="func_{obj.id}({obj.id})">View table</a>' \
                       f'<div id="table_{obj.id}"></div>' \
                       '<script>' \
                       'var count = 0;' \
                       f'function func_{obj.id}(id) ' \
                       '{{{{' \
                       f'var elem = document.getElementById("table_"+String(id));' \
                       'if(count === 0) {{{{elem.innerHTML = {0};count++;}}}}' \
                       'else {{{{elem.innerHTML = "";count--}}}}' \
                       '}}}}' \
                       '</script>'.format(html)
            return format_html(html_end)

    def activate_status_actions(self, request, queryset):
        count = 0
        for obj in queryset:
            count +=1
            obj.status = 'Active'
            obj.save()
        self.message_user(request, f"Установлен статус Active для {count} записей")
        return reverse('admin:cards_card_changelist'),


    activate_status_actions.short_description = 'Activate status'
    activate_status_actions.allow_tags = True

    def deactivate_status_actions(self, request, queryset):
        count = 0
        for obj in queryset:
            count +=1
            obj.status = 'Inactive'
            obj.save()
        self.message_user(request, f"Установлен статус Inactive для {count} записей")
        return reverse('admin:cards_card_changelist'),


    deactivate_status_actions.short_description = 'Deactivate status'
    deactivate_status_actions.allow_tags = True


admin.site.register(Card, WebsiteHistoryAdmin)
