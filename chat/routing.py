from django.urls import path
from . import consumers

ASGI_urlpatterns = [
    path("ws/<int:id>", consumers.ChatConsumer.as_asgi()),
]