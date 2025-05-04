from django.urls import path
from .consumers import ChatConsumer
from . import consumers

websocket_urlpatterns = [
    path(r'ws/chat/<str:room_name>/', ChatConsumer.as_asgi()),
    path(r'ws/video/(?P<room_name>\w+)/$', consumers.VideoChatConsumer.as_asgi()),
]
