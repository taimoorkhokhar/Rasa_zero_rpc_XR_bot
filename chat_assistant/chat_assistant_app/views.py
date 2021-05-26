from django.shortcuts import render
from chat_assistant_cms.db_queries import (
                                            get_all_collectives, 
                                            get_all_channel_assistants, 
                                            get_all_collective_channels
                                        )


def chat(request):
    all_collectives = get_all_collectives()
    all_assistant_list = []
    for collective_name in all_collectives:
        all_channels = get_all_collective_channels(collective_name)
        for channel_name in all_channels:
            assistants = get_all_channel_assistants(collective_name, channel_name)
            for assistant_dict in assistants:
                all_assistant_list.append({
                                assistant_dict['id']:
                                    [
                                        assistant_dict['assistant_name'],
                                        collective_name,
                                        channel_name
                                    ]
                                })
    
    context = {
                'all_assistants_detail'     : all_assistant_list
              }
    # Render the HTML template chat.html with the data in the context variable
    return render(request, 'chat.html', context)


