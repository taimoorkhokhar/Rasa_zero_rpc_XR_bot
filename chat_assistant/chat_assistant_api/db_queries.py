from .models import  Intent, Channel, Assistant, IntentExamples, Response
from django.forms.models import model_to_dict


def get_all_intent_names(assistant_id):
    assistant_obj = Assistant.objects.filter(id=assistant_id).first()
    all_intents   = Intent.objects.filter(assistant_id=assistant_obj).values_list('intent_name', flat=True)
    return list(all_intents)


def get_all_assistant_intents(**kwargs):
    """ Get intents and its corresponding example or 
        response sentences from database.
    Args: 
        assistant_id: Id of an assistant.
        sentence_type: if "example_sentence", returns intent and its example sententces. 
                       if "response_sentence", resturns intent and its response sentences 
                       from database.
    Returns:
        returns assistant name and example or response sentences
        depending on the argument sentence_type.
    
    """
    assistant_obj = Assistant.objects.filter(id=kwargs.get('assistant_id')).first()
    all_intents   = Intent.objects.filter(assistant_id=assistant_obj).all()
    if kwargs.get('sentence_type') == "example_sentence":
        all_examples_with_intents = get_all_intent_sentences(all_intents, IntentExamples, kwargs.get('sentence_type'))
        return all_examples_with_intents, assistant_obj.assistant_name
    elif kwargs.get('sentence_type') == "response_sentence":
        all_responses_with_intents = get_all_intent_sentences(all_intents, Response, kwargs.get('sentence_type'))
        return all_responses_with_intents, assistant_obj.assistant_name


def get_all_intent_sentences(intent_objs, model_obj, db_key):
    all_intent_examples = model_obj.objects.filter(intent_id__in=intent_objs)
    intent_list = [model_to_dict(intent) for intent in intent_objs]
    intent_dict = {}
    for intent in intent_list:
        intent_dict.update({intent['intent_name']:[]}) 
    for _ex in all_intent_examples:
        example = model_to_dict(_ex)
        intent_name = next(item for item in intent_list if item['id'] == example['intent_id'])
        intent_dict[intent_name['intent_name']].append(example[db_key])
    # print("intent_dict ", intent_dict)
    return intent_dict
