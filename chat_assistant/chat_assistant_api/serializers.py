from rest_framework import serializers
from . import models


class RequestTrainBotSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView."""
    id  = serializers.CharField(max_length=64)
    class Meta:
        fields = (
            'id',
        )


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Response
        fields = (
            'response_sentence',
        )
        
        
class IntentExamplesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IntentExamples
        fields = (
            'example_sentence',
        )
    

class IntentSerializer(serializers.ModelSerializer):
    example_sentences  = IntentExamplesSerializer(
                            read_only=True,
                            source='intentexamples_set',
                            many=True
                        )
    response_sentences = ResponseSerializer(
                            read_only=True,
                            source='response_set',
                            many=True
                        )
    
    class Meta:
        model = models.Intent
        fields = (
            'id' ,
            'intent_name',
            'example_sentences',
            'response_sentences'
        )


class AssistantSerializer(serializers.ModelSerializer):
    """Serializes a name field for testing our APIView."""
    intentExamples = IntentExamplesSerializer
    class Meta:
        model = models.Assistant
        fields = '__all__'
        depth = 2
    
    
    def create(self, validated_data):
        """Create and return a new Assistant."""

        assistant = models.Assistant.objects.create(
                        assistant_name=validated_data['assistant_name']
                    )
        
        return assistant
    
    
    def update(self, instance, validated_data):
        instance.assistant_name = validated_data.get('assistant_name')
        instance.save()
        
        return instance
        

class CreateAssistantSerializer(serializers.Serializer):
    collective_name = serializers.CharField(max_length=64)
    channel_name    = serializers.CharField(max_length=64)
    assistant_name  = serializers.CharField(max_length=64)
    id = serializers.IntegerField()


class ChannelSerializer(serializers.ModelSerializer):
    """Serializes a name field for testing our APIView."""
    class Meta:
        model = models.Channel
        fields = '__all__'
        depth = 1


class CreateChannelSerializer(serializers.Serializer):
    collective_name = serializers.CharField(max_length=64)
    channel_name    = serializers.CharField(max_length=64)
    
    class Meta:
        fields = (
            'collective_name',
            'channel_name'
        )

        
    def create(self, validated_data):
        """Create and return a new Channel."""
        collective_obj = models.Collective.objects.filter(
                            collective_name=validated_data['collective_name']
                        ).first()
        channel = models.Channel.objects.create(
                    channel_name=validated_data['channel_name'],
                    collective =collective_obj
                )
        return validated_data
    
    
class UpdateChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Channel
        fields = '__all__'
        depth = 2
        
        
    def update(self,instance,validated_data):
        instance.channel_name = validated_data.get('channel_name')
        instance.save()
        return instance


class CollectiveSerializer(serializers.ModelSerializer):
    """Serializes a name field for testing our APIView."""
    class Meta:
        model = models.Collective
        fields = '__all__'


class CreateCollectiveSerializer(serializers.ModelSerializer):
    """Serializes a name field for testing our APIView."""
    class Meta:
        model = models.Collective
        fields = (
            'collective_name',
        )
    
    
    def create(self, validated_data):
        """Create and return a new Collective."""

        collective = models.Collective.objects.create(
                        collective_name=validated_data['collective_name']
                    )
        
        return collective
    
    
    def update(self,instance,validated_data):
        instance.collective_name = validated_data.get('collective_name')
        instance.save()
        return instance


class UpdateCollectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Collective
        fields = (
            'collective_name',
        )
    
    
    def update(self,instance,validated_data):
        instance.collective_name = validated_data.get('collective_name')
        instance.save()
        return instance


class AskQuestionSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView."""
    id       = serializers.CharField(max_length=64)
    question = serializers.CharField(max_length=128)


class SessionSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(style={'input_type': 'password'})