# Create your  api views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import CartDetailSerializer
from .cart import Cart



class CartDetailAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        cart = Cart(request , request.user.username)
        items = [item for item in cart]
        ser_data = CartDetailSerializer(instance=items,many=True).data
        return Response(ser_data)



class CartAddAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self , request , course_slug):
        cart = Cart(request , request.user.username , course_slug)
        if request.session['course_data'][request.user.username][course_slug] != {}:
            return Response({"message":"You already have this course in your cart"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            cart.add(request)
        return Response({"message":"Your course has been added to cart successfully"},status=status.HTTP_200_OK)




class CartDeleteAPI(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self,request,course_slug):
        if request.session['course_data'][request.user.username].get(course_slug):
            cart = Cart(request,request.user.username , course_slug)
            cart.remove()
            return Response({"message":"Course has been removed from  cart"},status=status.HTTP_200_OK)
        return Response({"message":"You already don't have this course in your cart"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    