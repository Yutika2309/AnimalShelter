from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import (CreateAPIView, 
                                     ListCreateAPIView, 
                                     RetrieveUpdateAPIView, 
                                     RetrieveAPIView, 
                                     ListAPIView, 
                                     UpdateAPIView)

from rest_framework.response import Response
from rest_framework import viewsets, permissions, authentication
from rest_framework import status
from .serializers import * 

# Create your views here.
