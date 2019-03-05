from django.shortcuts import render
from SDOS_text.models import UserWithEmail
from SDOS_text.serializers import UserWithEmailSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class UserWithEmailAPI(APIView):
    def get(self, request, email, format=None):
        

