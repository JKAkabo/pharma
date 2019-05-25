from rest_framework import serializers

from .models import Stock


class StockSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Stock
        fields = ('units_sold', 'units_left')
