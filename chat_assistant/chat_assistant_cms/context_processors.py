import datetime
from .db_queries import get_all_collectives, get_all_channel_assistants, get_all_collective_channels

def get_collectives(request):
    all_collectives = get_all_collectives()
    collective_list = []
    for collective_name in all_collectives:
        all_channels = get_all_collective_channels(collective_name)
        collective_list.append({
            collective_name: all_channels
        })
    return {
        'collective_list': collective_list
    }


def get_channels(request):
    current_datetime = datetime.datetime.now()
    return {
        'channel_list': current_datetime.year
    }


def get_assistants(request):
    current_datetime = datetime.datetime.now()
    return {
        'assistant_list': current_datetime.year
    }