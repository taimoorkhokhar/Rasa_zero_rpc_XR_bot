from django.conf.urls import url
from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView
from rest_framework.authtoken import views as authviews
from . import views
from .core import collective as collective_views
from .core import channel as channel_views
from .core import assistant as assistant_views
app_name = 'chat_assistant_api'

router = DefaultRouter()

router.register('token', views.TokenViewSet, basename='token-authentication')
router.register('session', views.SessionViewSet, basename='session-authentication')

urlpatterns = [
    path('assistant/', assistant_views.Assistant.as_view()),
    path('assistant/<int:pk>/', assistant_views.UpdateAssistant.as_view()),
    path('ask-question/', assistant_views.AskQuestion.as_view()),
    path('train-assistant/', assistant_views.TrainAssistant.as_view()),
    path('channel/', channel_views.Channel.as_view()),
    path('channel/<int:pk>/', channel_views.UpdateChannel.as_view()),
    path('collective/', collective_views.Collective.as_view()),
    path('collective/<int:pk>/', collective_views.UpdateCollective.as_view()),
    path('', include(router.urls))
]