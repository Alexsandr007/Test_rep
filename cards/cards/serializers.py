from rest_framework import serializers

from .models import Card, Orders, DiscountPercent, Goods


class OrdersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Orders
        fields = ('number', 'sum',)


class DiscountPercentSerializer(serializers.ModelSerializer):

    class Meta:
        model = DiscountPercent
        fields = '__all__'



class GoodsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goods
        fields = '__all__'


class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = '__all__'
        depth = 2


