import pytest
import asyncio
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from app_quiz.consumers import RatingConsumer
from django.test import TransactionTestCase

User = get_user_model()

class TestRatingConsumer(TransactionTestCase):

    async def asyncSetUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
    @pytest.mark.asyncio
    async def test_connect_and_send_messages(self):
        communicator = WebsocketCommunicator(application, "/ws/rating/")  # путь маршрута
        communicator.scope['user'] = self.user
        connected, subprotocol = await communicator.connect()
        assert connected

        # Отправляем сообщение типа 'start'
        await communicator.send_json_to({'type': 'start', 'user': self.user.username})
        response = await communicator.receive_json_from()
        # Тут можно проверить, что получили ожидаемый ответ

        # Отправляем сообщение типа 'auth'
        await communicator.send_json_to({'type': 'auth', 'user': self.user.username})
        response2 = await communicator.receive_json_from()
        # Аналогично проверяем содержимое ответа

        # Можно отправить и другие сообщения, проверить ответы
        # Например, запрос таблицы рейтинга
        await communicator.send_json_to({'type': 'table', 'user': self.user.username})
        response3 = await communicator.receive_json_from()

        # Отключение
        await communicator.disconnect()