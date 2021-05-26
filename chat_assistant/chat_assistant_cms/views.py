from django.shortcuts import render
from .db_queries import *
import ast
from chat_assistant_api.db_queries import (
                                            get_all_assistant_intents, 
                                            get_all_intent_names, 
                                        )
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import csv
import json



def cms(request):
    # Render the HTML template dashboard.html with the data in the context variable
    return render(request, 'dashboard.html')


def create_channel(request):
    collective_name = request.GET.get('collective_name')
    channel_name = request.GET.get('channel_name')
    create_channel_in_db(collective_name, channel_name)
    # Render the HTML template dashboard.html with the data in the context variable
    return render(request, 'dashboard.html')


@csrf_exempt
def update_assistant_examples(request):
    if request.method == "POST":
        assistant_id = request.POST.get('assistant_id')
        data = request.POST.get('data')
        data_list = json.loads(data)
        for data_dict in data_list:
            for intent_name, data_to_change_dict in data_dict.items():
                questions_to_remove = data_to_change_dict['removedQuestions']
                responses_to_remove = data_to_change_dict['removedResponses']
                unsaved_questions   = data_to_change_dict['unsavedQuestions']
                unsaved_responses   = data_to_change_dict['unsavedResponses']
                delete_questions_of_intent(assistant_id,intent_name,questions_to_remove)
                delete_responses_of_intent(assistant_id,intent_name,responses_to_remove)
                update_assistant_example_query(assistant_id,intent_name,unsaved_questions,unsaved_responses)

        return JsonResponse({
                    'success': True
                })
    
    return JsonResponse({
                    'success': False
                })



@csrf_exempt
def upload_examples_csv(request, **kwargs):
    csv_file = request.FILES.get('csv_file')
    decoded_file = csv_file.read().decode('utf-8').splitlines()
    reader = csv.DictReader(decoded_file)
    for row in reader:
        intent = row.get('Intent','')
        questions = row.get('Example Questions','')
        questions_list = questions.split(',')
        response = row.get('Responses','')
        response_list =  [response]
        create_assistant_example(
                                    assistant_id=kwargs.get('assistant_id'),
                                    intent=intent,
                                    questions=questions_list,
                                    responses=response_list
                                )
    all_intent_examples, assistant_name = get_all_assistant_intents(    
                                                                        assistant_id=kwargs.get('assistant_id'),
                                                                        sentence_type='example_sentence'
                                                                    )
    all_intent_responses, assistant_name = get_all_assistant_intents(    
                                                                        assistant_id=kwargs.get('assistant_id'),
                                                                        sentence_type='response_sentence'
                                                                    )
    intent_example_response = []
    for intent, intent_examples in all_intent_examples.items():
        intent_responses = all_intent_responses[intent]
        intent_example_response.append({
                                        intent:[intent_examples, intent_responses]
                                    })

    context = {
                'intent_example_response' : intent_example_response,
                'assistant_name'          : assistant_name,
                'id'                      : kwargs.get('assistant_id')
            }

    return render(request, 'edit_assistant.html',context)


def view_assistant(request, **kwargs):
    all_intent_examples, assistant_name   = get_all_assistant_intents(    
                                                                        assistant_id=kwargs.get('assistant_id'),
                                                                        sentence_type='example_sentence'
                                                                    )
    all_intent_responses, assistant_name  = get_all_assistant_intents(    
                                                                        assistant_id=kwargs.get('assistant_id'),
                                                                        sentence_type='response_sentence'
                                                                    )
    
    intent_example_response = []
    for intent, intent_examples in all_intent_examples.items():
        intent_responses = all_intent_responses[intent]
        intent_example_response.append({
                                        intent:[intent_examples, intent_responses]
                                    })
    context = {
                'intent_example_response'   : intent_example_response,
                'assistant_name'            : assistant_name
              }

    # Render the HTML template view_assistant with the data in the context variable
    return render(request, 'view_assistant.html', context)


def add_assistant(request, **kwargs):
    assistant_id = request.GET.get('assistant_id')
    assistant_name = request.GET.get('assistant_name')
    create_assistant(
                        collective_name=kwargs.get('collective_name'),
                        channel_name=kwargs.get('channel_name'),
                        assistant_name=assistant_name,
                        assistant_id=assistant_id
                    )
    channel_assistants = get_all_channel_assistants(
                                                        kwargs.get('collective_name'),
                                                        kwargs.get('channel_name')
                                                    )

    context = {
                'assistants'     : channel_assistants,
                'channel_name'   : kwargs.get('channel_name'),
                'collective_name': kwargs.get('collective_name')
              }

    # Render the HTML template view_channel.html with the data in the context variable
    return render(request, 'view_channel.html', context)


def add_example(request, **kwargs):
    create_assistant_example(
                                assistant_id=kwargs.get('assistant_id'),
                                intent=request.GET.get('intent'),
                                questions=request.GET.getlist('questions'),
                                responses=request.GET.getlist('responses')
                            )
    all_intent_examples, assistant_name = get_all_assistant_intents(    
                                                                        assistant_id=kwargs.get('assistant_id'),
                                                                        sentence_type='example_sentence'
                                                                    )
    all_intent_responses, assistant_name = get_all_assistant_intents(
                                                                        assistant_id=kwargs.get('assistant_id'),
                                                                        sentence_type='response_sentence'
                                                                    )
    intent_example_response = []
    for intent, intent_examples in all_intent_examples.items():
        intent_responses = all_intent_responses[request.GET.get('intent')]
        intent_example_response.append({
                                        intent:[intent_examples, intent_responses]
                                    })

    context = {
                'intent_example_response' : intent_example_response,
                'assistant_name'          : assistant_name,
                'id'                      : kwargs.get('assistant_id')
              }

    # Render the HTML template edit_assistant.html with the data in the context variable
    return render(request, 'edit_assistant.html', context)


def edit_assistant(request, **kwargs):

    all_intent_examples, assistant_name = get_all_assistant_intents(    
                                                                        assistant_id=kwargs.get('assistant_id'),
                                                                        sentence_type='example_sentence'
                                                                    )
    all_intent_responses , assistant_name = get_all_assistant_intents(
                                                                        assistant_id=kwargs.get('assistant_id'),
                                                                        sentence_type='response_sentence'
                                                                    )
    intent_example_response = []
    for intent, intent_examples in all_intent_examples.items():
        intent_responses = all_intent_responses[intent]
        intent_example_response.append({
                                        intent:[intent_examples, intent_responses]
                                    })

    context = {
                'intent_example_response' : intent_example_response,
                'assistant_name'          : assistant_name,
                'id'                      : kwargs.get('assistant_id')
              }

    # Render the HTML template edit_assistant.html with the data in the context variable
    return render(request, 'edit_assistant.html', context)


def delete_assistant(request, assistant_id, assistants):
    assistant = delete_assistant_from_db(assistant_id)
    assistants =ast.literal_eval(assistants)
    [assistants.remove(_dict) for _dict in assistants if str(_dict.get('id',''))==str(assistant_id)]
    context = {
                'assistants'      : assistants,
                'channel_name'    : assistant.get('channel__channel_name'),
                'collective_name' : assistant.get('channel__collective__collective_name')
              }

    # Render the HTML template view_channel.html with the data in the context variable
    return render(request, 'view_channel.html', context)


def view_channel(request, collective_name, channel_name):
    channel_assistants = get_all_channel_assistants(collective_name, channel_name)

    context = {
                'assistants'      : channel_assistants,
                'channel_name'    : channel_name,
                'collective_name' : collective_name
              }

    # Render the HTML template view_channel.html with the data in the context variable
    return render(request, 'view_channel.html', context)

