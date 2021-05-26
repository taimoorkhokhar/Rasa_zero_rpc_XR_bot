from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.renderers import (
                                        HTMLFormRenderer, 
                                        JSONRenderer, 
                                        BrowsableAPIRenderer,
                                    )
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from celery.result import AsyncResult
from django.contrib import auth
from rasa.core.agent import Agent
from rasa.utils.endpoints import EndpointConfig
from rasa import train
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import asyncio
from .tasks import train_assistant_task
from . import serializers
from . import models

import logging
logging.basicConfig(level="DEBUG")


class TokenViewSet(viewsets.ViewSet):
    """Checks username and password and returns an auth token."""

    serializer_class = AuthTokenSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
        })



class SessionViewSet(viewsets.ViewSet):
    """Checks username and password and creates a user session."""

    serializer_class = serializers.SessionSerializer
    
    def create(self, request):
        """Use the ObtainAuthToken APIView to validate and create a token."""
        serializer = serializers.SessionSerializer(data=request.data)

        if serializer.is_valid():
            user_name = serializer.data.get('username')
            user_password = serializer.data.get('password')
            user = auth.authenticate(request, username=user_name, password=user_password)
            if user:
                if user.is_active:
                    auth.login(request, user)

                return Response({'response': 'Logged in'})
            return Response({'response':'Not Active User'})
        return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)