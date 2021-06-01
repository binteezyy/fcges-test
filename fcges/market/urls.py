from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers

from .api.transactions import StockViewSet, OrderViewSet, PortfolioView

api_router = routers.DefaultRouter(trailing_slash=False)
api_router.register('stocks', StockViewSet)
api_router.register('orders', OrderViewSet, basename='Orders')

urlpatterns = [
    path('', include(api_router.urls)),
    url(r'^portfolio$', PortfolioView.as_view(), name='Portfolio')
]

