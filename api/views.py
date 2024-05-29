from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import os
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import requests
import json
# Create your views here.

class IsActiveView(APIView):
    def get(self, request):
        data = {"message": "I Am Active, I Am Private Ollama!"}
        return Response(data, status=status.HTTP_200_OK)