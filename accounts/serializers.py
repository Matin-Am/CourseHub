from rest_framework import serializers
from .models import User



class UserRegisterationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(required=True,write_only=True)
    class Meta:
        model = User
        fields = ("username","email","password","password2")
        extra_kwargs = {
            "password":{"write_only":True}
        }

class UserVerifyCodeSerializer(serializers.Serializer):
    code = serializers.IntegerField(required=True)