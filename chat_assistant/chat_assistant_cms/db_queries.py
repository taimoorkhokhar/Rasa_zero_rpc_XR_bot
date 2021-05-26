from chat_assistant_api.models import Collective, Intent, Channel, Assistant, IntentExamples, Response
from django.forms.models import model_to_dict
import datetime


def get_all_collectives():
    all_collectives   = list(Collective.objects.values_list('collective_name', flat=True))
    return all_collectives


def get_all_collective_channels(collective_name):
    all_channels  = list(Channel.objects.filter(collective_id__collective_name=collective_name).values_list('channel_name', flat=True))
    return all_channels


def get_all_channel_assistants(collective_name, channel_name):
    channel_obj     = Channel.objects.filter(channel_name=channel_name, collective_id__collective_name=collective_name).first()
    all_asistants   = list(Assistant.objects.filter(channel_id=channel_obj).values('id','assistant_name'))
    print(all_asistants)
    return all_asistants


def create_assistant(*args, **kwargs):
    channel_obj     = Channel.objects.filter(
                                                channel_name=kwargs.get('channel_name'),
                                                collective_id__collective_name=kwargs.get('collective_name')
                                            ).first()
    Assistant.objects.create(
                                assistant_name=kwargs.get('assistant_name'),
                                id=kwargs.get('assistant_id'),
                                channel=channel_obj
                            )


def create_assistant_example(**kwargs):
    assistant_obj   = Assistant.objects.filter(id=kwargs.get('assistant_id')).first()
    intent_obj = Intent.objects.create(
                                        intent_name=kwargs.get('intent'),
                                        assistant_id=assistant_obj
                                        )
    for question in kwargs.get('questions'):
        question = question.replace('"',"'")
        IntentExamples.objects.create(example_sentence=question, intent_id=intent_obj)
    for response in kwargs.get('responses'):
        response = response.replace('"',"'")
        Response.objects.create(response_sentence=response, intent_id=intent_obj)


def create_channel_in_db(collective_name, channel_name):
    collective_obj     = Collective.objects.filter(collective_name=collective_name).first()
    Channel.objects.create(channel_name=channel_name, collective=collective_obj)


def delete_questions_of_intent(assistant_id, intent, questions):
    assistant_obj   = Assistant.objects.filter(id=assistant_id).first()
    intent_obj      = Intent.objects.filter(intent_name=intent, assistant_id=assistant_obj).first()
    for question in questions:
        IntentExamples.objects.filter(example_sentence=question,intent_id=intent_obj).delete()


def delete_responses_of_intent(assistant_id, intent, responses):
    assistant_obj   = Assistant.objects.filter(id=assistant_id).first()
    intent_obj      = Intent.objects.filter(intent_name=intent, assistant_id=assistant_obj).first()
    for response in responses:
        Response.objects.filter(response_sentence=response,intent_id=intent_obj).delete()


def update_assistant_example_query(assistant_id, intent, questions, responses):
    assistant_obj   = Assistant.objects.filter(id=assistant_id).first()
    intent_obj = Intent.objects.filter(intent_name=intent, assistant_id=assistant_obj).first()
    for question in questions:
        question = question.replace('"',"'")
        IntentExamples.objects.create(example_sentence=question, intent_id=intent_obj)
    for response in responses:
        response = response.replace('"',"'")
        Response.objects.create(response_sentence=response, intent_id=intent_obj)


def delete_assistant_from_db(assistant_id):
    assistant_obj = Assistant.objects.values('assistant_name','channel__channel_name','channel__collective__collective_name').get(id=assistant_id)
    Assistant.objects.filter(id=assistant_id).delete()
    return assistant_obj