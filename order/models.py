from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator , MaxValueValidator
from django.utils import timezone
# Create your models here.



class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE , related_name='orders')
    total_price = models.IntegerField()
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    discount = models.IntegerField(null=True , blank=True , default=None)

    def __str__(self):
        return str(self.id)
    
    def apply_discount(self):
        discount_price = (self.discount/100) * self.total_price
        self.total_price = self.total_price - discount_price
        return self.total_price

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE , related_name='items')
    title = models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self):
        return f"{self.title}- {self.order}"
    
class Coupon(models.Model):
    code = models.CharField(max_length=30 , unique=True)
    discount = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(90)])
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=False)


    def __str__(self):
        return self.code
    
