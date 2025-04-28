from rest_framework import serializers
from .models import Course , Episode
from accounts.models import User
from accounts.serializers import UserRegisterationSerializer



class CourseSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = '__all__'
    def get_user(self , obj):
        users = User.objects.all()
        return UserRegisterationSerializer(instance=users , many=True).data


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = '__all__'