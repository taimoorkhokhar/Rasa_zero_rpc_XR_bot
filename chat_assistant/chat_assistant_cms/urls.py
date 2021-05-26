from django.conf.urls import url
from django.conf.urls import include

from rest_framework.routers import DefaultRouter
from django.conf.urls import url
from django.urls import path
from chat_assistant_cms import views
app_name = 'chat_assistant_cms'

urlpatterns = [
    path('add_example/<str:assistant_id>', views.add_example, name='add_example'),
    path('upload_examples_csv/<str:assistant_id>', views.upload_examples_csv, name='upload_examples_csv'),
    path('view_assistant/<str:assistant_id>', views.view_assistant, name='view_assistant'),
    path('edit_assistant/<str:assistant_id>', views.edit_assistant, name='edit_assistant'),
    path('update_assistant_examples', views.update_assistant_examples, name='update_assistant_examples'),
    path('delete_assistant/<str:assistant_id>/<str:assistants>', views.delete_assistant, name='delete_assistant'),
    path('view_channel/<str:collective_name>/<str:channel_name>', views.view_channel, name='view_channel'),
    path('create_channel/', views.create_channel, name='create_channel'),
    path('add_assistant/<str:collective_name>/<str:channel_name>', views.add_assistant, name='add_assistant'),
    url('', views.cms, name='cms'),
]
