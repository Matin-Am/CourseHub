from rest_framework import serializers
from .models import Order , OrderItem
from accounts.models import User
from accounts.serializers import UserRegisterationSerializer



class CartDetailSerializer(serializers.Serializer):
    title = serializers.CharField()
    price = serializers.CharField()
    add_time = serializers.CharField()


class OrderDetailSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Order
        fields = ("user","total_price","paid","created")

