# Create your  api views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import CartDetailSerializer , OrderDetailSerializer
from .models import Order , OrderItem
from django.shortcuts import get_object_or_404
from .cart import Cart


class CartDetailAPI(APIView):
    """
    displays the detail of user s' cart
    """
    serializer_class = CartDetailSerializer
    permission_classes = [IsAuthenticated]
    def get(self,request):
        cart = Cart(request , request.user.username)
        items = [item for item in cart]
        ser_data = self.serializer_class(instance=items,many=True).data
        return Response(ser_data, status=status.HTTP_200_OK)



class CartAddAPI(APIView):
    """
    Add a course to the user s' cart 
    """
    permission_classes = [IsAuthenticated]
    def post(self , request , course_slug):
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
        return Response({"message":"You already don't have this course in your cart"},status=status.HTTP_400_BAD_REQUEST)



class OrderDetailAPI(APIView):
    """
    Shows the detail of user s' order
    """
    serialzier_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]
    def get(self,request,order_id):
        order = get_object_or_404(Order , id=order_id , user=request.user)
        ser_data = self.serialzier_class(instance=order).data
        return Response(ser_data , status=status.HTTP_200_OK)
    
class OrderCreateAPI(APIView):
    """
    Creates  a new order for user that contains all selected courses in user s' cart
    """
    permission_classes = [IsAuthenticated]
    def post(self,request):
        session = request.session
        cart = Cart(request,request.user.username)
        if not cart:
            return Response({"message": "Your cart is empty."}, status=status.HTTP_400_BAD_REQUEST)
        order = Order.objects.create(user=request.user , total_price=cart.get_total_price())
        for item in session['course_data'][request.user.username].values():
            OrderItem.objects.create(order=order , title=item['title'] , price=item['price'])
        cart.clear()
        return Response({"message":"Order has been created successfully",
                         "order_id":order.id}
                         ,status=status.HTTP_201_CREATED)