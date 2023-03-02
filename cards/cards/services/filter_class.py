from django_filters import DateTimeFilter, FilterSet
from ..models import Orders, Card


class OrdersFilter(FilterSet):
    from_date = DateTimeFilter(field_name='date',
                                             lookup_expr='gte')
    to_date = DateTimeFilter(field_name='date',
                                           lookup_expr='lte')
    class Meta:
        model = Orders
        fields = ['from_date','to_date',]


class CardsFilter(FilterSet):
    from_created= DateTimeFilter(field_name='created_at',
                                             lookup_expr='gte')
    to_created = DateTimeFilter(field_name='created_at',
                                           lookup_expr='lte')
    from_date_end = DateTimeFilter(field_name='date_end',
                                             lookup_expr='gte')
    to_date_end = DateTimeFilter(field_name='date_end',
                                           lookup_expr='lte')
    class Meta:
        model = Card
        fields = ['from_created','to_created','from_date_end','to_date_end']
