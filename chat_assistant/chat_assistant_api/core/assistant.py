from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
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
from ..tasks import train_assistant_task
from .. import serializers
from .. import models
from ..apps import ProfilesApiConfig
import torch
import asyncio


@csrf_exempt
def get_assistant_response(assistant_id, question):
    agent = ProfilesApiConfig.agents.get(assistant_id)
    if agent.is_ready():
        loop = asyncio.get_event_loop()
        reply = loop.run_until_complete(agent.handle_text(question))
        agent_response_data = agent.tracker_store.retrieve_full_tracker("default")._latest_message_data()
        intent = agent_response_data.get('intent',{})

        return reply, intent



def generate_response(tokenizer, model, chat_round, chat_history_ids, question):
    """
        Generate a response to some user input.
    """
    # Encode user input and End-of-String (EOS) token
    new_input_ids = tokenizer.encode(">> You: "+ question + tokenizer.eos_token, return_tensors='pt')

    # Append tokens to chat history
    bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1) if chat_round > 0 else new_input_ids

    # Generate response given maximum chat length history of 1250 tokens
    chat_history_ids = model.generate(bot_input_ids, max_length=1250, pad_token_id=tokenizer.eos_token_id)
    
    # Print response
    print("DialoGPT: {}".format(tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)))
    
    response = format(tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True))
    
    # Return the chat history ids
    # return chat_history_ids
    return response


class Assistant(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CreateAssistantSerializer
    

    def get(self, request):
        assistants = models.Assistant.objects.all()
        serializer = serializers.AssistantSerializer(assistants, many=True)
        a_viewset = [
            'Uses actions (GET, POST)',
        ]

        return Response({'a_viewset': a_viewset, 'response': serializer.data})


    def post(self, request):
        serializer = serializers.CreateAssistantSerializer(data=request.data)
        if serializer.is_valid():
            collective_name = serializer.data.get('collective_name')
            channel_name = serializer.data.get('channel_name')
            assistant_name = serializer.data.get('assistant_name')
            assistant_id = serializer.data.get('id')
            channel_obj     = models.Channel.objects.filter(channel_name=channel_name, collective_id__collective_name=collective_name).first()
            models.Assistant.objects.create(assistant_name=assistant_name, id=assistant_id, channel=channel_obj)
            
            a_viewset = [
                'Uses actions (GET, POST)',
            ]

            return Response({'a_viewset': a_viewset, 'response': serializer.data})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateAssistant(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.AssistantSerializer

    def get(self, request, pk):
        try:
            assistant = models.Assistant.objects.get(id=pk)
            intent_examples = models.Intent.objects.filter(assistant_id=assistant)
            intent_serializer = serializers.IntentSerializer(intent_examples, many=True)
            serializer = serializers.AssistantSerializer(assistant)

            an_apiview = [
                'Uses HTTP methods as function (get, put, delete)',
            ]
            
            if not intent_serializer.data:
                return Response({'an_apiview': an_apiview, 'response': serializer.data})

            return Response({'an_apiview': an_apiview, 'response': intent_serializer.data})
        except:
            
            return Response({'response':'404 Not Found'})
    
    
    def put(self, request, pk):
        """Handles updating an object."""
        serializer = serializers.AssistantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'response':serializer.data})
        return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        try:
            assistant = models.Assistant.objects.filter(id=pk).delete()
            return JsonResponse({
                    'success': True, "response": "deleted"
                })
        except:
            return Response({'success': False, 'response': '404'})
        
        

class TrainAssistant(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.RequestTrainBotSerializer


    def get(self, request, format=None):
        """Returns a list of APIView features."""

        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put, delete)',
            'It is similar to a traditional Django view',
            'Gives you the most control over your logic',
            'Is mapped manually to URLs'
        ]

        if 'task_id' in request.GET:
            task_id = request.query_params['task_id']
            result = AsyncResult(task_id)
            response_data = {
                'state': result.state,
                'details': result.info,
            }
        else:
            assistants = models.Assistant.objects.all()
            serializer = serializers.AssistantSerializer(assistants, many=True)
            response_data = serializer.data

        return Response(response_data)


    def post(self, request):

        serializer = serializers.RequestTrainBotSerializer(data=request.data)

        if serializer.is_valid():
            assistant_id = serializer.data.get('id')
            task = train_assistant_task.delay(assistant_id=assistant_id)

            return JsonResponse({"response": task.task_id})
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AskQuestion(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.AskQuestionSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, HTMLFormRenderer)
    

    def get(self, request, format=None):
        """Returns a list of APIView features."""

        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put, delete)',
            'It is similar to a traditional Django view',
            'Gives you the most control over your logic',
            'Is mapped manually to URLs'
        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview})


    def post(self, request):
        """Create a hello message with our name."""

        serializer = serializers.AskQuestionSerializer(data=request.data)

        if serializer.is_valid():
            assistant_id = serializer.data.get('id')
            question = serializer.data.get('question')
            assistant_response, intent = get_assistant_response(assistant_id, question)
            confidence = intent.get('confidence', 0)

            if assistant_response and confidence >= 0.20:
                return Response({assistant_id: assistant_response[0].get("text")})
            else:
                # tokenizer, model = load_tokenizer_and_model()
                # Initialize history variable
                chat_history_ids = None
                chat_round = 0
                response = generate_response(ProfilesApiConfig.tokenizer, ProfilesApiConfig.gpt_model, chat_round, chat_history_ids, question)
                return Response({assistant_id: response})
        else:
            return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
