
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('chat_assistant_api.urls')),
    url(r'^app/', include('chat_assistant_app.urls')),
    url(r'^cms/', include('chat_assistant_cms.urls')),
]
