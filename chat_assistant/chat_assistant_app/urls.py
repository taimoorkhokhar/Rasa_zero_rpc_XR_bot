from django.conf.urls import url
from . import views

urlpatterns = [
    url('', views.chat, name='chat'),
    url('^chat/', views.chat, name='chat'),
]
