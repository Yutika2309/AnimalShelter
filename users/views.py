from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView, 
    ListCreateAPIView,
    CreateAPIView,
    DestroyAPIView
)
from .serializers import SignupSerializer, LoginSerializer
from core.models import ShelterUser

# Create your views here.


class SignupView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token = None
        try:
            token = Token.objects.get(user=user)
        except:
            token = Token.objects.create(user=user)

        return Response({'token': token.key}, status=status.HTTP_200_OK)


class LoginView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = ShelterUser.objects.filter(email=email).first()
        # print("USER_OBJ_HERE:", user.email, user.password)
        if user and user.check_password(password):
            token = None
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)
            return Response({'message':'Logged in successfully.', 'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error':'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
