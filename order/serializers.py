from rest_framework import serializers







class CartDetailSerializer(serializers.Serializer):
    title = serializers.CharField()
    price = serializers.CharField()
    add_time = serializers.CharField()