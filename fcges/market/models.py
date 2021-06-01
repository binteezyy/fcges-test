from django.db import models
from django.contrib.auth.models import User

# Create your models here.
ACTION_CHOICES = (
    (0, 'Buy'),
    (1, 'Sell'),
)

class Stock(models.Model):
    name = models.CharField(max_length=122)
    code = models.CharField(max_length=6)
    price = models.DecimalField(decimal_places=4, max_digits=10)

    def __str__(self):
        return f'{self.code} - {self.price}'

    class Meta:
        unique_together = ['name', 'code']

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=4, max_digits=10)
    quantity = models.PositiveBigIntegerField(default=1)
    action = models.IntegerField(choices=ACTION_CHOICES)