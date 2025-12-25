from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import threading
import time
import random


def index(request):
    return render(request, 'index.html')

def user_quiz(request):
    return render(request, 'user_page.html')

def start_updating():
    def update_loop():
        channel_layer = get_channel_layer()
        users = ['Иван', 'Петр', 'Алексей', 'Мария']
        while True:
            time.sleep(1)  # обновлять каждые 5 секунд
            rating = []
            for user in users:
                rating.append({
                    'user': user,
                    'score': random.randint(0, 100),
                    'time': round(random.uniform(10, 60), 2)
                })
            # Отправляем обновление всем слушателям
            async_to_sync(channel_layer.group_send)(
                'rating_updates',
                {
                    'type': 'send_rating_update',
                    'message': rating
                }
            )
    thread = thread


# Когда кто-то отвечает правильно, вы отправляете сообщение в группу:

import asyncio

async def send_update():
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        'rating_updates',
        {
            'type': 'send_rating_update',
            'message': {'type': 'update', 'content': 'Обновление рейтинга'}
        }
    )

# вызов из async функции
# asyncio.run(send_update())


