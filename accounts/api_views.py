from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegisterationSerializer , UserVerifyCodeSerializer
from .models import User , OtpCode
from utils import Data 
from .tasks import send_otp
import random
import pytz 
from datetime import datetime

class UserRegistrationAPI(APIView):
    """
    Sending  a code to user for authentication terms
    """
    serializer_class = UserRegisterationSerializer
    def post(self,request):
        ser_data = self.serializer_class(data=request.data)
        if ser_data.is_valid():
            cd = ser_data.validated_data
            random_code = random.randint(1000 , 9999)
            current_time = str(datetime.now(tz=pytz.timezone('Asia/Tehran')))
            OtpCode.objects.create(code=random_code,email=cd['email'])
            send_otp.apply_async(args=[cd['email'], random_code])
            data = Data(request,cd['username'],current_time)
            data.save_data(cd['email'],cd['password'])
            return Response({"message":"We sent you a code please check your email"},status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserVerifyCodeAPI(APIView):
    """
    Completing user s' registration process
    """
    serializer_class = UserVerifyCodeSerializer
    def post(self,request):
        session = request.session['user_data']
        ser_data  = self.serializer_class(data=request.data)
        username_session = list(session.keys())[-1]
        if ser_data.is_valid():
            instance_code = get_object_or_404(OtpCode , email=session[username_session]['email'])
            if instance_code.is_expired():
                return Response({"message":"code is expired"},status=status.HTTP_408_REQUEST_TIMEOUT)
            if ser_data.validated_data['code'] == instance_code.code:
                user = User.objects.create_user(
                    username=username_session , 
                    email=session[username_session]['email'],
                    password=session[username_session]['password']
                )
                del session[username_session]
                return Response(UserRegisterationSerializer(user).data,status=status.HTTP_201_CREATED)
            else:
                return Response({"message":"code is wrong"},status=status.HTTP_400_BAD_REQUEST)
            
class LogOutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"mesaage":"Logged out successfully"},status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"Error":str(e)}, status=status.HTTP_400_BAD_REQUEST)