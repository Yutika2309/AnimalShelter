from django.shortcuts import render
from rest_framework.response import Response
from .serializers import AnimalOnboardingSerializer
from core.models import AnimalOnboarding
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
from rest_framework.pagination import PageNumberPagination

# Create your views here.

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class OnboardedAnimalsView(ListAPIView):

    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]
    pagination_class = StandardResultsSetPagination

    def get(self, request, *args, **kwargs):
        queryset = AnimalOnboarding.objects.all()
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = AnimalOnboardingSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = AnimalOnboardingSerializer(queryset, many=True)
        return Response(serializer.data)
    