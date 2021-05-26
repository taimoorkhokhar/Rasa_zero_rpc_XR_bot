from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.http import JsonResponse, HttpResponse
from .. import serializers
from .. import models



class Channel(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CreateChannelSerializer
    

    def get(self, request):
        channels = models.Channel.objects.all()
        serializer = serializers.ChannelSerializer(channels, many=True)
        
        a_viewset = [
            'Uses actions (GET, POST)',
        ]

        return Response({'a_viewset': a_viewset, 'response': serializer.data})


    def post(self, request):
        serializer = serializers.CreateChannelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            a_viewset = [
                'Uses actions (GET, POST)',
            ]
            
            return Response({'a_viewset': a_viewset, 'response': serializer.data})
        return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateChannel(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UpdateChannelSerializer
    def get(self, request, pk):
        try:
            channel = models.Channel.objects.get(id=pk)
            
            serializer = serializers.UpdateChannelSerializer(channel)

            an_apiview = [
                'Uses HTTP methods as function (get, put, delete)',
            ]

            return Response({'an_apiview': an_apiview, 'response': serializer.data})
        except:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, validated_data):
            return models.Channel.create(**validated_data)
    
    def put(self, request, pk):
        """Handles updating an object."""
        channel = models.Channel.objects.get(id=pk)
        serializer = serializers.UpdateChannelSerializer(instance=channel,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'response':serializer.data})
        return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        try:
            Channel = models.Channel.objects.filter(id=pk).delete()
            return JsonResponse({
                    'success': True, "response": "deleted"
                })
        except:
            return Response({'success': False, 'response': '404'})