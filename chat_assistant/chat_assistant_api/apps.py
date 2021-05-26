from django.apps import AppConfig
from django.conf import settings
import os
from transformers import AutoModelForCausalLM, AutoTokenizer
from rasa.core.agent import Agent
from rasa.utils.endpoints import EndpointConfig


class ProfilesApiConfig(AppConfig):
    name = 'chat_assistant_api'
    
    # Initialize tokenizer and model
    print("Loading GPTDialog model...")
    tokenizer = AutoTokenizer.from_pretrained(settings.MODELS)
    gpt_model = AutoModelForCausalLM.from_pretrained(settings.MODELS)
    
    print("Loading Rasa Assistant models...")
    models = os.listdir(settings.RASA_MODELS)
    agents = {}
    for model in models:
        load_model = settings.RASA_MODELS + model
        agent = Agent.load(load_model, action_endpoint=EndpointConfig(settings.ACTION_ENDPOINT))
        model_id = model.split(".")[0]
        agents.update(
                       {str(model_id):agent}
                      )