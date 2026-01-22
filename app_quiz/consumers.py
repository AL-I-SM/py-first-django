import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from .models import UserProgress, Answer, Question
from datetime import datetime, timezone
from classbook.models import User
import zoneinfo
from asgiref.sync import sync_to_async


class RatingConsumer(AsyncWebsocketConsumer):
    

    # завершение теста, когда все прошли
    # страница преподвателя
    # передать общее количество вопросов и пройденный вопрос или вообще весь болк сразу
    # красивости
      
    # ratings = {}
    print("RatingConsumer создан")
    
    # должны быть доработки вроде users_and_rating['название канала'],
    # или что-то аналогичное для работы нескольких тестов одновременно
    users_and_rating = {}
    groups_started = {}
    

    def __init__(self , *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("экземпляр RatingConsumer создан")

    async def connect(self):
        print(self.scope)
        self.user = self.scope["user"]
        self.group_name = 'rating' ###
        self.channel_layer = get_channel_layer() #???

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        if self.user.is_anonymous:
            await self.close()
        else:
            await self.accept()
   
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_rating_table(self, event):
        print('таблица рейтинга отправлена')
        await self.send(text_data=event['message'])

    async def send_question_data(self, event):
        print('вопрос отправлен')
        await self.send(text_data=event['message'])
       
    @database_sync_to_async
    def get_question(self, number, subject_id, packet):
        return Question.objects.get(number=number, subject_id=subject_id, packet=packet)
    
    async def send_to_layer_group(self, user, content, type, type_data):

        data = {
            'user': str(user),
            'type': type,                       # соответствует обработчику на JS
            'content': content                  # данные (должны быть сериализуемы в JSON)
        }

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': type_data,
                'message': json.dumps(data)
            }
        )

    async def receive(self, text_data):
        
        data = json.loads(text_data)
        message_type = data.get("type")
        user = data.get('user', 'Аноним')
        user_name = str(user)

        print(self.users_and_rating, self.channel_layer)

        if message_type == 'start':

            # можно еще принимать вермя старта от каждого клиента
            
            # добавляет начавшийся тест и время его начала в общий словарь
            self.groups_started.update({self.group_name: datetime.now()})
            await self.send_to_layer_group(user_name, str(datetime.now()),
                                            'start', 'send_rating_table')

        if message_type == 'auth':
            self.users_and_rating.update({user_name: {"score": 0, 
                                                 "time": 0,
                                                 "number": 1,
                                                 "subject_id": 1,
                                                 "packet": 1}})
            
            await self.send_to_layer_group(user_name, self.users_and_rating,
                                           'rating_updates', 'send_rating_table')
       
        if message_type == 'table':
            print('запрошена таблица рейтинга') 
            
            await self.send_to_layer_group(user_name, self.users_and_rating,
                                           'rating_table', 'send_rating_table')

            '''
            data = {
                'type': 'rating_table',             # соответствует обработчику на JS
                'content': self.users_and_rating   # данные (должны быть сериализуемы в JSON)
            }

            await self.channel_layer.group_send(
                'rating',
                {
                    'type': 'send_rating_table',
                    'message': json.dumps(data)
                }
            )
            '''
        
        if message_type == 'question':
            # если тест начался, то он в словаре, иначе вопрос не отправляется
            if self.group_name in self.groups_started:
        
                number_inc = 1 if data.get("state") == 'next' else 0

                number = self.users_and_rating[user_name]['number']
                number += number_inc
                subject_id = self.users_and_rating[user_name]['subject_id']
                packet = self.users_and_rating[user_name]['packet'] 
                score = self.users_and_rating[user_name]['score']
                packet = self.users_and_rating[user_name]['packet']
                time_taken = self.users_and_rating[user_name]['time']
                
                print(user_name, number, subject_id, packet)

                question_obj = False
                try:
                    question_obj = await self.get_question(number, subject_id, packet)
                except Exception as e:
                    print(f'данне вопроса не получены: {e}')
                    await self.send_to_layer_group(user_name, score,
                                                'end_test', 'send_rating_table')

                    student = await database_sync_to_async(User.objects.get)(username=user_name)
                    # get_or_create
                    # если завершение теста, то сохранение общего прогресса прользователя
                    await database_sync_to_async(UserProgress.objects.create)(
                        user=student,
                        score=score,
                        packet=packet,
                        time_taken = time_taken,
                        date = datetime.now()
                    )

                    # удалить пользователя из теста
                    del self.users_and_rating[user_name]
                    print("пользователь закончил тест")
                    
                    if not self.users_and_rating:
                        del self.groups_started[self.group_name]


                if question_obj:
                    question = {
                        
                        'text': question_obj.text,
                        'options': question_obj.options,
                        'number': question_obj.number,
                        'correct': question_obj.correct_answer,
                        'question_id': question_obj.id
                    }

                    print(question)
                    
                    self.users_and_rating[user_name]['number'] = number
                    
                    await self.send_to_layer_group(user_name, question,
                                                'question', 'send_question_data')

        if message_type == 'answer':
            answer = data.get("answer")
            question_id = data.get("question_id")
            answered_at = data.get("answered_at")
            print(f'получен ответ: {answer} в {answered_at}') 
            
            answered_at_server =  datetime.now()

            try:
                student = await database_sync_to_async(User.objects.get)(username=user_name)
            except Exception as e:
                print(f'пользователь с таким username не найден: {e}')
                student = None

            is_correct = None
            try:
                question_obj =  await sync_to_async(Question.objects.get)(id=question_id)
                correct_answer = question_obj.correct_answer
                if answer:
                    if answer == correct_answer:
                        is_correct = True
                    else:
                        is_correct = False   

            except Exception as e:
                print(f'вопроса с таким ID нет в базе данных: {e}')
                question_obj = None

            format = "%Y-%m-%dT%H:%M:%S.%fZ"
            time_answer = datetime.strptime(answered_at, format).replace(tzinfo=timezone.utc)
            start =  self.groups_started[self.group_name].astimezone(zoneinfo.ZoneInfo("Europe/Moscow"))
            seconds = abs((time_answer - start).total_seconds())
            self.users_and_rating[user_name]['time'] = seconds

            # Записываем ответ
            await database_sync_to_async(Answer.objects.create)(
                user=student,
                question_id=question_id,
                answer=answer,
                answered_at_server=answered_at_server,
                answered_at_client=time_answer,
                is_correct=is_correct
            )
            
            if question_obj and is_correct:
                self.users_and_rating[user_name]['score'] += question_obj.score

            # Обновляем рейтинг
            await self.send_to_layer_group(user_name, self.users_and_rating,
                                           'rating_updates', 'send_rating_table')
