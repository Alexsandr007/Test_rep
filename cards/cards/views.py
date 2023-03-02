from django.http import HttpResponseRedirect
from .models import gen_smth
from .models import Card, DiscountPercent, Orders, Goods
from rest_framework.viewsets import ModelViewSet
from .serializers import CardSerializer, OrdersSerializer, DiscountPercentSerializer, GoodsSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
import schedule
import datetime
from .services.filter_class import OrdersFilter, CardsFilter

def generate_cards(request):
    print(request.POST)
    if request.POST['number'] == '':
        return HttpResponseRedirect("/cards/card/")
    for i in range(int(request.POST['number'])):
        percent = DiscountPercent.objects.get(name='default')
        card = Card(series=request.POST['series'],number=gen_smth(3),created_at=request.POST['date_start_0'],date_end=request.POST['date_end_0'],summa_purchases=0,status='Active',percent=percent)
        card.save()
    return HttpResponseRedirect("/admin/cards/card/")


class DiscountPercentViewSet(ModelViewSet):
    queryset = DiscountPercent.objects.all()
    serializer_class = DiscountPercentSerializer


class OrdersViewSet(ModelViewSet):
    serializer_class = OrdersSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = OrdersFilter


class GoodsViewSet(ModelViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer


class CardViewSet(ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CardsFilter

    @action(detail=True, methods=['post'], serializer_class=OrdersSerializer)
    def add_order(self, request, pk):
        card = self.get_object()
        if card.status != 'Overdue':
            serializer = OrdersSerializer(data=request.data)
            print(serializer)
            if serializer.is_valid():
                order = Orders.objects.create(
                    number=serializer.validated_data['number'],
                    sum=serializer.validated_data['sum'],
                )
                order.save()
                for obj in serializer.validated_data['goods']:
                    goods = Goods.objects.create(
                        name=obj['name'],
                        cost=obj['cost'],
                        discount_cost=obj['discount_cost']
                    )
                    goods.save()
                    order.goods.add(goods)
                order.save()
                return Response({'status': 'adding order complete'})
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)


def status_check():
    cards = Card.objects.all()
    for i in cards:
        if i.status == 'Active' or i.status == 'Inactive' or i.status == 'Frozen':
            if i.date_end >= datetime.date.today():
                i.status = 'Overdue'
                i.save()


schedule.every().day.at("08:00").do(status_check)
