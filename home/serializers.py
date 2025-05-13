from rest_framework import serializers
from .models import Course , Episode
from accounts.models import User
from .models import Comment
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

class CommentSerializer(serializers.ModelSerializer):
    course = serializers.SlugRelatedField(slug_field='slug',read_only=True)
    class Meta:
        model = Comment
        fields = ("user","course","reply","is_reply","text")
        extra_kwargs = {
            "text":{"required":True},
        } 

    def create(self, validated_data):
        request = self.context['request']
        parent_comment = self.context.get("parent_comment")
        course = self.context['course']
        comment = Comment.objects.create(
            user=request.user ,
            course = course ,
            reply = parent_comment, 
            is_reply = bool(parent_comment) ,
            text = validated_data['text']
        )
        return comment