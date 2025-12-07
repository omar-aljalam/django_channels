from django.urls import path
from . import consumers

ASGI_urlpatterns = [
    path("ws/", consumers.ChatConsumer.as_asgi()),
]