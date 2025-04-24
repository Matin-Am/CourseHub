from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Course , Episode
from .serializers import CourseSerializer , EpisodeSerializer
from rest_framework import status



class CourseListAPI(APIView):
    def get(self,request):
        courses = Course.objects.all()
        ser_data = CourseSerializer(instance=courses , many=True)
        return Response(ser_data.data , status=status.HTTP_200_OK)

class CourseDetailAPI(APIView):
    def get(self,request , course_slug):
        course = get_object_or_404(Course , slug=course_slug)
        ser_data = CourseSerializer(instance=course)
        return Response(ser_data.data, status=status.HTTP_200_OK)
    
class EpisodeDetailAPI(APIView):
    def get(self, request , epi_slug):
        episode = get_object_or_404(Episode , slug=epi_slug )
        if  request.user not in episode.course.user.all() and not episode.course.paid :
            return Response({"message":"You can't watch this video"}, status=status.HTTP_403_FORBIDDEN)
        ser_data = EpisodeSerializer(instance=episode).data
        return Response(ser_data,status=status.HTTP_200_OK)
