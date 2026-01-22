from channels.auth import AuthMiddlewareStack
from django.urls import re_path
from .consumers import RatingConsumer

websocket_urlpatterns = [
    re_path(r'ws/rating/$', AuthMiddlewareStack(RatingConsumer.as_asgi())),
]