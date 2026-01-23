import pytest
import asyncio
from django.contrib.auth import get_user_model
from django.test import TransactionTestCase
from classbook.models import User, Disciplines
from app_quiz.models import Question
from asgiref.sync import sync_to_async
from channels.layers import get_channel_layer


from django.test import TestCase
from channels.testing import WebsocketCommunicator
from app_quiz.consumers import RatingConsumer
from datetime import datetime, timezone

class TestRatingConsumer(TestCase):


    async def сonnect_communicator(self):
        user = await sync_to_async(User.objects.create_user)(
            username='testuser', password='testpassword'
        )
        login_successful = await sync_to_async(self.client.login)(username='testuser', password='testpassword')
        communicator = WebsocketCommunicator(RatingConsumer.as_asgi(), "/ws/rating/")
        communicator.scope['user'] = user
        connected, _ = await communicator.connect()
        return (communicator, connected, login_successful)
        

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
    async def test_connect(self):
        communicator, connected, login_successful = await self.сonnect_communicator()

        assert connected
        assert login_successful

        await communicator.disconnect()
        

    @pytest.mark.asyncio
    async def test_send_message_auth(self):
        communicator, _, _ = await self.сonnect_communicator()
        
        user = communicator.scope['user']

        # Отправляем сообщение типа 'auth'
        await communicator.send_json_to({'type': 'auth', 'user': user.username})
        response = await communicator.receive_json_from()
        # Аналогично проверяем содержимое ответа

        assert len(response) == 3
        assert response['type'] == 'rating_updates'
        assert len(response['content']['testuser']) == 5
        assert response['user'] == 'testuser'

        await communicator.disconnect()


    @pytest.mark.asyncio
    async def test_send_message_start(self):
        communicator, connected, login_successful = await self.сonnect_communicator()
        assert connected
        assert login_successful
        
        user = communicator.scope['user']

        # Отправляем сообщение типа 'start'
        await communicator.send_json_to({'type': 'start', 'user': user.username})
        response = await communicator.receive_json_from()

        assert len(response) == 3
        assert response['type'] == 'start'
        assert response['user'] == 'testuser'
        assert len(response['content']) == 26

        await communicator.disconnect()


    @pytest.mark.asyncio
    async def test_send_message_table(self):
        communicator, _, _ = await self.сonnect_communicator()
        
        user = communicator.scope['user']    

        await communicator.send_json_to({'type': 'table', 'user': user.username})
        response = await communicator.receive_json_from()
        
        assert len(response) == 3
        assert response['type'] == 'rating_table'
        assert len(response['content']['testuser']) == 5
        assert response['user'] == 'testuser'

        await communicator.disconnect()
    

    @pytest.mark.asyncio    
    async def test_no_action_if_send_message_question_with_no_start(self):
        communicator, _, _ = await self.сonnect_communicator()
        
        user = communicator.scope['user'] 

        question = await sync_to_async(Question.objects.create)(subject_id = 1,
                                                                text = "text1",
                                                                number = 1,
                                                                options = ["1", "2"],
                                                                correct_answer = "1",
                                                                packet = 1,
                                                                score = 1)
        subject = await sync_to_async(Disciplines.objects.create)(name = "disciplines1")

        # запрос вопроса, когда в БД есть данные, но еще тест не начался
        # ответ не должен приходить
        try:
            await communicator.send_json_to({'type': 'question', 'user': user.username})
            await communicator.receive_json_from()
        
            assert False, "Expected exception was not raised"

        except TimeoutError:
            pass

 
    @pytest.mark.asyncio
    async def test_send_message_question(self):
        communicator, _, _ = await self.сonnect_communicator()
        
        user = communicator.scope['user'] 

        await communicator.send_json_to({'type': 'auth', 'user': user.username})
        response = await communicator.receive_json_from()
        await communicator.send_json_to({'type': 'start', 'user': user.username})
        response = await communicator.receive_json_from()


        question = await sync_to_async(Question.objects.create)(subject_id = 1,
                                                                text = "text1",
                                                                number = 1,
                                                                options = ["1", "2"],
                                                                correct_answer = "1",
                                                                packet = 1,
                                                                score = 1)
        subject = await sync_to_async(Disciplines.objects.create)(name = "disciplines1")

        # запрос вопроса, когда в БД есть данные
        await communicator.send_json_to({'type': 'question', 'user': user.username})
        response = await communicator.receive_json_from()

        assert len(response) == 3
        assert response['type'] == 'question'
        assert len(response['content']) == 5
        assert response['user'] == 'testuser'  

        await communicator.disconnect()


    @pytest.mark.asyncio
    async def test_send_message_answer(self):
        communicator, _, _ = await self.сonnect_communicator()
        
        user = communicator.scope['user']

        await communicator.send_json_to({'type': 'auth', 'user': user.username})
        response = await communicator.receive_json_from()
        await communicator.send_json_to({'type': 'start', 'user': user.username})
        response = await communicator.receive_json_from()

        question = await sync_to_async(Question.objects.create)(subject_id = 1,
                                                                text = "text1",
                                                                number = 1,
                                                                options = ["1", "2"],
                                                                correct_answer = "1",
                                                                packet = 1,
                                                                score = 1)
        subject = await sync_to_async(Disciplines.objects.create)(name = "disciplines1")

        await communicator.send_json_to({'type': 'answer',
                                         'answered_at': datetime.now(timezone.utc).isoformat(timespec='microseconds').replace('+00:00', 'Z'),
                                         'user': user.username,
                                         'question_id': 1,
                                         'answer': "answer1"})
        response = await communicator.receive_json_from()

        assert len(response) == 3
        assert response['type'] == 'rating_updates'
        assert len(response['content']['testuser']) == 5
        assert response['user'] == 'testuser'
      
        # Отключение
        await communicator.disconnect()


    @pytest.mark.asyncio
    async def test_end_quiz_if_no_questions(self):
        communicator, _, _ = await self.сonnect_communicator()
        
        user = communicator.scope['user']

        await communicator.send_json_to({'type': 'auth', 'user': user.username})
        response = await communicator.receive_json_from()
        await communicator.send_json_to({'type': 'start', 'user': user.username})
        response = await communicator.receive_json_from()

        # запрос вопроса, когда в БД нет данных
        # он так же удалит пользователя из словаря рейтинга (как проверить?)

        await communicator.send_json_to({'type': 'question', 'user': user.username})
        response = await communicator.receive_json_from()

        assert len(response) == 3
        assert response['type'] == 'end_test'
        assert response['content'] == 0
        assert response['user'] == 'testuser'
        
          
        '''
        try:
            # если исключение не возникло, то тест не прошел
            assert False, "Expected exception was not raised"

        except TimeoutError:
            # исключение было вызвано — тест прошел
            pass
        '''
