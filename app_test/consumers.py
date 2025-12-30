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
    
    users_and_rating = {}
    # ratings = {}
    start_time = datetime.now()
    started = False
    
    async def connect(self):
        self.user = self.scope["user"]._wrapped 
        self.group_name = 'rating' ###
        # self.group_name = "quiz_group"
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

    async def send_rating_update(self, event):
        print('данне общего рейтинга обновлены')
        await self.send(text_data=event['message'])

    async def send_rating_table(self, event):
        print('таблица рейтинга отправлена')
        await self.send(text_data=event['message'])

    async def send_question_data(self, event):
        print('следующий вопрос отправлен')
        await self.send(text_data=event['message'])
       
    @database_sync_to_async
    def get_question(self, number, subject_id, packet):
        return Question.objects.get(number=number, subject_id=subject_id, packet=packet)
    
    async def send_to_layer_group(self, content, type, type_data):

        data = {
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

        print(self.users_and_rating, self.channel_layer)

        if message_type == 'start':
            # можно еще принимать вермя старта от каждого клиента
            if not self.started:
                self.started = True
                await self.send_to_layer_group(str(datetime.now()),
                                              'start', 'send_rating_update')

        if message_type == 'auth':
            self.users_and_rating.update({user: {"score": 0, 
                                                  "time": 0,
                                                  "number": 0,
                                                  "subject_id": 1,
                                                  "packet": 1}})
            
            await self.send_to_layer_group(self.users_and_rating,
                                           'rating_updates', 'send_rating_update')

            '''
            data = {
                'type': 'rating_updates',           # соответствует обработчику на JS
                'content': self.users_and_rating   # данные (должны быть сериализуемы в JSON)
            }

            await self.channel_layer.group_send(
                'rating',                           # название канала группы
                {
                    'type': 'send_rating_update',
                    'message': json.dumps(data)
                }
            )
            print(self.users_and_rating)
            '''
        
        if message_type == 'table':
            print('запрошена таблица рейтинга') 
            
            await self.send_to_layer_group(self.users_and_rating,
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
        
        if message_type == 'next_question':
            
            number = self.users_and_rating[user]['number']
            number += 1
            subject_id = self.users_and_rating[user]['subject_id']
            packet = self.users_and_rating[user]['packet'] 
            score = self.users_and_rating[user]['score']
            packet = self.users_and_rating[user]['packet']
            time_taken = self.users_and_rating[user]['time']
            
            question_obj = False
            try:
                question_obj = await self.get_question(number, subject_id, packet)
            except Exception as e:
                print(f'данне вопроса не получены: {e}')
                await self.send_to_layer_group(score,
                                              'end_test', 'send_rating_update')

                '''
                data = {
                    'type': 'end_test',                # соответствует обработчику на JS
                    'content': score                   # данные (должны быть сериализуемы в JSON)
                }
                await self.channel_layer.group_send(
                    'rating',
                    {
                        'type': 'send_question_data',
                        'message': json.dumps(data)
                    }
                )
            '''
                
                student = await database_sync_to_async(User.objects.get)(username=user)
                # get_or_create
                await database_sync_to_async(UserProgress.objects.create)(
                    user=student,
                    score=score,
                    packet=packet,
                    time_taken = time_taken,
                    date = datetime.now()
                ) 


            if question_obj:
                question = {
                    'text': question_obj.text,
                    'options': question_obj.options,
                    'number': question_obj.number,
                    'correct': question_obj.correct_answer,
                    'question_id': question_obj.id
                }

                print(question)
                
                self.users_and_rating[user]['number'] = number
                
                await self.send_to_layer_group(question,
                                               'next_question', 'send_question_data')

                '''
                data = {
                    'type': 'next_question',             # соответствует обработчику на JS
                    'content': question                  # данные (должны быть сериализуемы в JSON)
                }

                await self.channel_layer.group_send(
                    'rating',
                    {
                        'type': 'send_question_data',
                        'message': json.dumps(data)
                    }
                )
                '''

        if message_type == 'answer':
            answer = data.get("answer")
            question_id = data.get("question_id")
            answered_at = data.get("answered_at")
            print(f'получен ответ: {answer} в {answered_at}') 
            
            answered_at_server =  datetime.now()

            try:
                student = await database_sync_to_async(User.objects.get)(username=user)
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
            start = self.start_time.astimezone(zoneinfo.ZoneInfo("Europe/Moscow"))
            seconds = abs((time_answer - start).total_seconds())
            self.users_and_rating[user]['time'] = seconds

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
                self.users_and_rating[user]['score'] += question_obj.score

            # Обновляем рейтинг
            await self.send_to_layer_group(self.users_and_rating,
                                           'rating_updates', 'send_rating_update')

            '''
            data = {
                'type': 'rating_updates',           # соответствует обработчику на JS
                'content': self.users_and_rating   # данные (должны быть сериализуемы в JSON)
            }

            await self.channel_layer.group_send(
                'rating',                           # название канала группы
                {
                    'type': 'send_rating_update',
                    'message': json.dumps(data)
                }
            )
        
            '''
        