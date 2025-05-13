from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status , viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .serializers import CourseSerializer , EpisodeSerializer , CommentSerializer
from .models import Course , Episode , Comment
from .custome_permissions import IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404 , get_list_or_404

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


# class CommentAPI(APIView):
#     permission_classes = [IsAuthenticated]
#     def post(self,request,course_slug, comment_id=None):
#         parrent_comment = None
#         course = get_object_or_404(Course , slug=course_slug)
#         if comment_id:
#             parrent_comment = get_object_or_404(Comment,id=comment_id)
#         ser_data = CommentSerializer(data=request.data,context={"request":request,"course":course,"parrent_comment":parrent_comment})
#         if ser_data.is_valid():
#             comment = ser_data.save()
#             return Response(CommentSerializer(comment).data,status=status.HTTP_201_CREATED)
#         return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST) 
    
# class CommentDeleteAPI(APIView):
#     permission_classes = [IsOwnerOrReadOnly]
#     def delete(self,request,comment_id):
#         comment = get_object_or_404(Comment ,pk=comment_id)
#         comment.delete()
#         return Response({"message":"Comment has been deleted successfully"},status=status.HTTP_200_OK)
    
# class CommentListAPI(APIView):
#     def get(self,request,course_slug):
#         course = get_object_or_404(Course , slug=course_slug)
#         comments = course.c_comments.all()
#         ser_data = CommentSerializer(instance=comments, many=True)
#         return Response(ser_data.data , status=status.HTTP_200_OK)

class CommentViewSet(viewsets.ModelViewSet):
    """
    This viewset handles making , listing and deleting comments
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]
    @action(detail=False, methods=['post'], url_path=r'create_comment/(?P<course_slug>[^/.]+)(?:/(?P<comment_id>\d+))?')
    def make_comment(self,request,course_slug,comment_id=None):
        parent_comment = None
        course = get_object_or_404(Course , slug=course_slug)
        if comment_id:
            parent_comment = get_object_or_404(Comment,id=comment_id)
        ser_data = CommentSerializer(data=request.data,context={"request":request,"course":course,"parent_comment":parent_comment})
        if ser_data.is_valid():
            comment = ser_data.save()
            return Response(CommentSerializer(comment).data,status=status.HTTP_201_CREATED)
        return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST) 
    
    @action(detail=False , methods=["get"],url_path=r'(?P<course_slug>[^/.]+)')
    def list_comments(self,request,course_slug):
        course = get_object_or_404(Course , slug=course_slug)
        comments = course.c_comments.all()
        ser_data = CommentSerializer(instance=comments, many=True).data
        return Response(ser_data , status=status.HTTP_200_OK)

