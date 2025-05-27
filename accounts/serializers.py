from rest_framework import serializers
from .models import User
from rest_framework import validators


def clean_username(value):
    if value == 'admin':
        raise serializers.ValidationError("Your username cant be admin,Please choose another username")


class UserRegisterationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(required=True,write_only=True,label='confirm password')
    class Meta:
        model = User
        fields = ("username","email","password","password2")
        extra_kwargs = {
            "password":{"write_only":True,"required":True},
            "username":{"required":True,"validators":[clean_username,]},
            "email":{"required":True},

        }

    def validate_username(self,value):
        users = User.objects.filter(username=value).exists()
        if users:
            raise serializers.ValidationError('This username already exists')
        return value



    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords must match !!!")
        return data

class UserVerifyCodeSerializer(serializers.Serializer):
    code = serializers.IntegerField(required=True)


