import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from .models import UserProgress, Answer, Question
import datetime
from classbook.models import User


class RatingConsumer(AsyncWebsocketConsumer):
    
    users_and_ratings = {}
    
    async def connect(self):
        self.user = self.scope["user"]._wrapped 
        self.group_name = 'rating' # важно!
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
            self.progress, created = await self.get_or_create_progress(self.user)
    

    @database_sync_to_async
    def get_or_create_progress(self, user):
        print(user)
        return UserProgress.objects.get_or_create(user=self.user, packet=1)
        

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
            'rating',
            {
                'type': type_data,
                'message': json.dumps(data)
            }
        )


    async def receive(self, text_data):
        
        data = json.loads(text_data)
        message_type = data.get("type")
        user = data.get('user', 'Аноним')

        print(self.users_and_ratings, self.channel_layer)

        if message_type == 'auth':
            self.users_and_ratings.update({user: {"score": 0, 
                                                  "time": 0,
                                                  "number": 0,
                                                  "subject_id": 1,
                                                  "packet": 1}})
            
            await self.send_to_layer_group(self.users_and_ratings,
                                           'rating_updates', 'send_rating_update')

            '''
            data = {
                'type': 'rating_updates',           # соответствует обработчику на JS
                'content': self.users_and_ratings   # данные (должны быть сериализуемы в JSON)
            }

            await self.channel_layer.group_send(
                'rating',                           # название канала группы
                {
                    'type': 'send_rating_update',
                    'message': json.dumps(data)
                }
            )
            print(self.users_and_ratings)
            '''
        
        if message_type == 'table':
            print('запрошена таблица рейтинга') 
            
            await self.send_to_layer_group(self.users_and_ratings,
                                           'rating_table', 'send_rating_table')

            '''
            data = {
                'type': 'rating_table',             # соответствует обработчику на JS
                'content': self.users_and_ratings   # данные (должны быть сериализуемы в JSON)
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
            
            number = self.users_and_ratings[user]['number']
            number += 1
            subject_id = self.users_and_ratings[user]['subject_id']
            packet = self.users_and_ratings[user]['packet'] 
            
            question_obj = False
            try:
                question_obj = await self.get_question(number=number, subject_id=1, packet=1)
            except:

                data = {
                    'type': 'end_test',                # соответствует обработчику на JS
                    'content': 'user_rating'           # данные (должны быть сериализуемы в JSON)
                }
                await self.channel_layer.group_send(
                'rating',
                {
                    'type': 'send_question_data',
                    'message': json.dumps(data)
                }
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
                
                self.users_and_ratings[user]['number'] = number
                
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
            print(f'получен ответ: {answer}') 

            try:
                student = await database_sync_to_async(User.objects.get)(username=user)
            except User.DoesNotExist:
                student = None

            is_correct = None
            try:
                question_obj =  await database_sync_to_async(Question.objects.get)(id=question_id)
                correct_answer = question_obj.correct_answer
                if answer:
                    if answer == correct_answer:
                        is_correct = True
                    else:
                        is_correct = False   

            except User.DoesNotExist:
                student = None

            # Записываем ответ
            await database_sync_to_async(Answer.objects.create)(
                user=student,
                question_id=question_id,
                answer=answer,
                answered_at=datetime.datetime.now(),
                is_correct=is_correct

            )
           
            await self.send_to_layer_group(self.users_and_ratings,
                                           'rating_updates', 'send_rating_update')

            '''
            data = {
                'type': 'rating_updates',           # соответствует обработчику на JS
                'content': self.users_and_ratings   # данные (должны быть сериализуемы в JSON)
            }

            await self.channel_layer.group_send(
                'rating',                           # название канала группы
                {
                    'type': 'send_rating_update',
                    'message': json.dumps(data)
                }
            )
        
            '''
        
        '''


        # Обновляем прогресс
        next_question = await self.get_next_question(self.student, question)
        if next_question:
            # Обновляем прогресс
            await database_sync_to_async(
                lambda: UserProgress.objects.filter(student=self.student).update(current_question=next_question)
            )
            # Отправляем следующий вопрос
            await self.send_question(next_question)
        else:
            # Тест завершен
            await self.send(json.dumps({"message": "Тест завершен"}))
            # Можно отключить или оставить для общего прогресса

        # Рассылаем обновление прогресса всем
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'update_progress',
                'student': self.student.username,
                'status': 'answered'
            }
        )
        
        ###
        current_question = progress.current_question
        if current_question:
            await self.send_question(current_question)
        else:
            # Если вопросов нет или завершено
            await self.send(json.dumps({"message": "Тест завершен"}))
        '''


    async def update_progress(self, event):
        # Обработка обновления прогресса для всех
        await self.send(text_data=json.dumps({
            'message': f"{event['student']} ответил и переходит к следующему вопросу."
        }))


    @database_sync_to_async
    def get_next_question(self, user, current_question):
        # Логика получения следующего вопроса
        questions = list(Question.objects.all().order_by('id'))
        try:
            index = questions.index(current_question)
            return questions[index + 1]
        except (ValueError, IndexError):
            return None