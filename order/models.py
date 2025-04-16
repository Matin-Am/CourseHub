from django.db import models
from django.conf import settings
# Create your models here.



class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE , related_name='orders')
    total_price = models.IntegerField()
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE , related_name='items')
    title = models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self):
        return f"{self.title}- {self.order}"