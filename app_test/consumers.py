import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer


class RatingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'rating_updates'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_rating_update(self, event):
        await self.send(text_data=json.dumps(event['message']))

    async def receive(self, text_data):
        data = json.loads(text_data)
        answer = data.get('answer')
        user = data.get('user', 'Аноним')

        # Логика оценки ответа
        # Например, если ответ правильный:
        correct_answer = 'Париж'
        score_increment = 10 if answer.strip().lower() == correct_answer.lower() else 0

        # Обновление данных рейтинга
        # Предположим, у вас есть какая-то структура хранения
        # Для этого примера — просто отправляем обновление всем

        # Можно сохранить результат в базе или памяти (упрощено)
        # Тогда пересчитывайте рейтинг и рассылайте обновление

        # Для демонстрации — просто отправляем сообщение всем
        # В реальной системе нужно обновлять рейтинг в базе и пересылать обновленный список

        # Например, имитируем обновление
        # (здесь можно интегрировать с моделями)

        # Отправляем новую таблицу рейтинга всем
        rating = [
            {"user": "Иван", "score": 50, "time": 15},
            {"user": "Петр", "score": 30, "time": 20},
            {"user": user, "score": score_increment, "time": 5}
        ]
        await self.channel_layer.group_send(
            'rating_updates',
            {
                'type': 'send_rating_update',
                'message': rating
            }
        )