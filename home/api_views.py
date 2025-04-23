from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Course
from .serializers import CourseSerializer
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