from django.conf.urls import url
from bot.views import CommandReceiver


urlpatterns = [
    url(r'^tok/(?P<bot_token>.+)/$', CommandReceiver.as_view(), name="command"),
]