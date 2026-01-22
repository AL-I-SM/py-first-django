import pytest
import asyncio
from django.contrib.auth import get_user_model
from django.test import TransactionTestCase
from classbook.models import User
from asgiref.sync import sync_to_async
from channels.layers import get_channel_layer


from django.test import TestCase
from channels.testing import WebsocketCommunicator
from app_quiz.consumers import RatingConsumer

class TestRatingConsumer(TestCase):

    def get_user(self):
        # Создаем тестового пользователя
        user =  User.objects.create_user(username='teacher1',
                                         first_name='Иван',
                                         last_name='Иванов',
                                         middle_name='Иванович'
                                        )
        return user
    

    @pytest.fixture
    def auto_login_user(db, client, create_user, test_password):
        def make_auto_login(user=None):
            if user:
                client.logout()
            if user is None:
                user = create_user()
            client.login(username=user.username, password=test_password)
            return client, user
        return make_auto_login


    @pytest.mark.asyncio
    async def test_connect_and_send_messages(self):
        user = await sync_to_async(User.objects.create_user)(
             username='testuser', password='testpassword'
        )
        # user = await sync_to_async(self.get_user)()
        communicator = WebsocketCommunicator(RatingConsumer.as_asgi(), "/ws/rating/")
        communicator.scope['user'] = user
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