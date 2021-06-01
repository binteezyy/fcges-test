from django.conf import settings
from django.db.models import F, Sum, Case, When, DecimalField
from rest_framework import serializers, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Stock, Order, ACTION_CHOICES

from collections import defaultdict

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

class ActionChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        return self._choices[obj]

class OrderSerializer(serializers.ModelSerializer):
    action = ActionChoiceField(choices=ACTION_CHOICES)
    class Meta:
        model = Order
        exclude = ('user', )

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        instance = super(OrderSerializer, self).create(validated_data)

        return instance

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class PortfolioView(APIView):

    def post(self, request):
        user_orders = Order.objects.filter(user=request.user).values('stock__id', 'stock__name', 'action')\
                        .annotate(total=Sum(F('price') * F('quantity')), quantity=Sum(F('quantity'))).order_by()

        totals = {
            'overall_investment': 0,
            'overall_realized_pnl': 0,
            'overall_unrealized_pnl': 0,
            'stocks': {}
        }
        for order in user_orders:
            stock_id = str(order['stock__id'])
            
            if stock_id not in totals['stocks'].keys():
                totals['stocks'][stock_id] = {}
                totals['stocks'][stock_id]['name'] = order['stock__name']
                totals['stocks'][stock_id]['total_amount_invested'] = 0 
                totals['stocks'][stock_id]['quantity'] = 0
                totals['stocks'][stock_id]['realized_pnl'] = 0
                totals['stocks'][stock_id]['unrealized_pnl'] = 0

            if order['action'] == 0:
                totals['stocks'][stock_id]['total_amount_invested'] += order['total']
                totals['stocks'][stock_id]['quantity'] += order['quantity']
                totals['overall_investment'] += order['total']
                
            else:
                totals['stocks'][stock_id]['realized_pnl'] += order['total']
                totals['stocks'][stock_id]['quantity'] -= order['quantity']
                totals['overall_realized_pnl'] += order['total']

        for key, value in totals['stocks'].items():
            amount = value['total_amount_invested'] - value['realized_pnl'] + (value['quantity'] * Stock.objects.get(id=key).price)
            totals['stocks'][key]['unrealized_pnl'] += amount
            totals['overall_unrealized_pnl'] += amount


        return Response(totals)
