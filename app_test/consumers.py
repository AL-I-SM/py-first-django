import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

class RatingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # добавляем пользователя в группу
        self.group_name = 'rating_updates'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # удаляем из группы
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # вызывается, когда в группе есть сообщение
    async def send_rating_update(self, event):
        await self.send(text_data=json.dumps(event['message']))

    # Метод для получения сообщений из других частей кода и рассылки
    async def receive(self, text_data):
        # необязательно, если клиенты только слушают
        pass