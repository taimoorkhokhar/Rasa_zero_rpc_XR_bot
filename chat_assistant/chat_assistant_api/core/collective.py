from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.http import JsonResponse, HttpResponse
from .. import serializers
from .. import models


class Collective(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CollectiveSerializer


    def get(self, request):
        collective = models.Collective.objects.all()
        serializer = serializers.CollectiveSerializer(collective, many=True)   
        a_viewset = [
            'Uses actions (GET, POST)',
        ]

        return Response({'a_viewset': a_viewset, 'response': serializer.data})
    
    
    def post(self, request):
        serializer = serializers.CreateCollectiveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            a_viewset = [
                'Uses actions (GET, POST)',
            ]

            return Response({'a_viewset': a_viewset, 'response': serializer.data})
        return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateCollective(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UpdateCollectiveSerializer
    
    
    def get(self, request, pk):
        try:
            collective = models.Collective.objects.get(id=pk)
            serializer = serializers.CollectiveSerializer(collective)
            an_apiview = [
                'Uses HTTP methods as function (get, put, delete)',
            ]

            return Response({'an_apiview': an_apiview, 'response': serializer.data})
        except:
            return Response({'response':'Collective not found'})
    
    
    def create(self, validated_data):
        return models.Collective.create(**validated_data)
        
        
    def put(self, request, pk):
        """Handles updating an object."""
        collective = models.Collective.objects.get(id=pk)
        serializer = serializers.UpdateCollectiveSerializer(instance=collective,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'response':serializer.data})
        return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )


    def delete(self, request, pk):
        try:
            collective = models.Collective.objects.filter(id=pk).delete()
            return JsonResponse({
                    'success': True,
                    "response": "deleted"
                })
        except:
            return Response({
                    'success': False,
                    'response': '404'
                })