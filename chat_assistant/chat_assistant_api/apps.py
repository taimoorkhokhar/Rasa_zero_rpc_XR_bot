from django.apps import AppConfig
from django.conf import settings
from transformers import AutoModelForCausalLM, AutoTokenizer
from django.db.models.signals import post_migrate
from django.contrib.auth.apps import AuthConfig
from django.contrib.auth.models import User


USERNAME = "super_reality_user"
PASSWORD = "super_reality"


def create_test_user(sender, **kwargs):
    if not settings.DEBUG:
        return
    if not isinstance(sender, AuthConfig):
        return
    manager = User.objects
    try:
        manager.get(username=USERNAME)
    except User.DoesNotExist:
        manager.create_superuser(USERNAME, 'nick@gamegen.com', PASSWORD)


class RasaApiConfig(AppConfig):
    name = 'chat_assistant_api'
    
    # Initialize tokenizer and model
    print("Loading GPTDialog model...")
    tokenizer = AutoTokenizer.from_pretrained(settings.MODELS)
    gpt_model = AutoModelForCausalLM.from_pretrained(settings.MODELS)
    def ready(self):
        post_migrate.connect(create_test_user)