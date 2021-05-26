from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
import jsonfield


class Collective(models.Model):
    """Super Reality Organizations."""

    collective_name = models.CharField(max_length=64)


class Channel(models.Model):
    """Channels inside Super Reality Organizations."""

    channel_name  = models.CharField(max_length=64)
    collective = models.ForeignKey(Collective, on_delete=models.CASCADE)


class Assistant(models.Model):
    """Rasa AI Assistant for Each Channel."""
    
    id = models.IntegerField(primary_key=True) 
    assistant_name = models.CharField(max_length=128)
    channel     = models.ForeignKey(Channel, on_delete=models.CASCADE)


class Intent(models.Model):
    """Intent."""

    intent_name = models.CharField(max_length=1024)
    assistant_id = models.ForeignKey(Assistant, on_delete=models.CASCADE)


class Response(models.Model):
    """Response for intent."""

    response_sentence = models.CharField(max_length=4096)
    intent_id         = models.ForeignKey(Intent, on_delete=models.CASCADE)
    

class IntentExamples(models.Model):
    """Example sentences for intent."""

    example_sentence = models.CharField(max_length=2048)
    intent_id        = models.ForeignKey(Intent, on_delete=models.CASCADE)
