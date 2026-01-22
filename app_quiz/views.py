from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.decorators import login_required
import threading
import time
import random

menu = {}
  
def index(request):
    return render(request, 'quiz.html')


@login_required
def user_quiz(request):

    context = {'user': request.user,
               'all_menu': menu}
    return render(request, 'quiz_user_page.html', context)



