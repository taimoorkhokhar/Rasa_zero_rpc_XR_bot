from __future__ import unicode_literals
import os
import yaml
import ruamel.yaml
from rasa.train import train
from celery import shared_task
from django.views.decorators.csrf import csrf_exempt
from .db_queries import (
                            get_all_assistant_intents, 
                            get_all_intent_names
                        )


@csrf_exempt
def create_rasa_nlu(all_intent_examples):
    nlu_data = 'version: "2.0" \nnlu:'
    for key, values in all_intent_examples.items():
        nlu_data += "\n - intent: " + key
        nlu_data += "\n   examples: | \n"
        for value in values:
            nlu_data += "      - " + value + "\n"

    yaml = ruamel.yaml.YAML()
    code = yaml.load(nlu_data)
    yaml.default_flow_style = False
    yaml.indent(sequence=4, offset=2)
    with open('rasa/data/nlu.yml', 'w') as yaml_file:
        yaml.dump(code, yaml_file)


@csrf_exempt
def create_rasa_stories(all_intents):
    nlu_data = {"stories": []}
    for intent in all_intents:
        story_dict = {'story': intent.replace("_", " "),
                      'steps': [
                          {'intent': intent},
                          {'action': 'utter_' + intent}
                      ]
                      }
        nlu_data['stories'].append(story_dict)
    with open('rasa/data/stories.yml', 'w') as yaml_file:
        yaml.dump(nlu_data, yaml_file, sort_keys=False)



@csrf_exempt
def create_rasa_domain(all_intent_responses):
    nlu_data = {"session_config": {'session_expiration_time': 60, 'carry_over_slots_to_new_session': True}}
    all_intents = list(all_intent_responses.keys())
    nlu_data.update({"intents": all_intents})
    responses = {}
    for key, values in all_intent_responses.items():
        list_of_dicts = []
        for _list_text in values:
            list_of_dicts.append({'text': _list_text})
        responses.update({"utter_" + key: list_of_dicts})

    nlu_data.update({"responses": responses})
    with open('rasa/domain.yml', 'w') as yaml_file:
        yaml.dump(nlu_data, yaml_file, sort_keys=False)



def train_dialogue_model(training_data_folder,domain_path,config_file_path, output_path,model_name):
    full_modal_path = output_path+model_name+".tar.gz"
    if os.path.isfile(full_modal_path):
        os.remove(full_modal_path)
    train(
        domain=domain_path,
        config=config_file_path,
        training_files=training_data_folder,
        output=output_path,
        fixed_model_name=model_name,
        force_training=False,
    )



@shared_task(name='train_assistant_task', bind=True)
def train_assistant_task(self, **kwargs):
    all_intent_examples,assistant_name = get_all_assistant_intents(    
                                                                        assistant_id=kwargs.get('assistant_id'),
                                                                        sentence_type='example_sentence'
                                                                    )
    all_intent_responses,assistant_name = get_all_assistant_intents(    
                                                                        assistant_id=kwargs.get('assistant_id'),
                                                                        sentence_type='response_sentence'
                                                                    )

    all_intents = get_all_intent_names(kwargs.get('assistant_id'))
    create_rasa_nlu(all_intent_examples)
    create_rasa_domain(all_intent_responses)
    create_rasa_stories(all_intents)
    domain_path          = "rasa/domain.yml"
    training_data_folder = "rasa/data"
    config_file_path     = "rasa/config.yml"
    output_path			 = "rasa/models/"
    model_name	 = kwargs.get('assistant_id').replace(" ", "")
    train_dialogue_model(training_data_folder,domain_path,config_file_path, output_path,model_name)
    return "Training Completed"
