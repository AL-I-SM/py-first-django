from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse, reverse_lazy
from .models import Topic
from .forms import TopicForm, EntryForm, Entry
from django.contrib.auth.decorators import login_required


menu = {}
'''
<h4><a href="admin/">'admin' - Админка средствами Django</a></h4>
<h4><a href="classbook/">'classbook' - Классный журнал</a></h4>
<h4><a href="catalog/">'catalog' - Книжная библиотека</a></h4>
<h4><a href="projects/">'projects' - Тут сделать фото-галерею!</a></h4>
<h4><a href="topics/">'topics' - Блога (основная база пользователей)</a></h4>
<h4><a href="blog/">'blog'- Блога</a></h4>
<h4><a href="users/login/">'users' - Авторизация пользователей</a></h4>
<h4><a href="players/dashboard/">'players' - Простая форма отправки данных + Авторизация</a></h4>
<h4><a href="cards/">'cards' - Непонятный проект из Githab</a></h4>
<h4><a href="days/">'days' - в разработке</a></h4>
<h4><a href="quizz/">'quizz' - в разработке</a></h4>
<br> 
'''

def index(request):
    return render(request, 'topics.html', {'all_menu': menu})


@login_required
def topics(request):
    # topics = Topic.objects.all().order_by('date_added')
    if request.user.is_superuser:
        topics = Topic.objects.all().order_by('date_added')
    else:
        topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics,
               'all_menu': menu}
    return render(request, 'topics.html', context)


@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    topics = Topic.objects.all().order_by('date_added')
    if not request.user.is_superuser:
        if topic.owner != request.user:
            raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'topics': topics, 'entries': entries,
               'user': request.user, 'person': topic.owner, 'all_menu': menu}
    return render(request, 'topic.html', context)


@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
        return HttpResponseRedirect(reverse('topics'))
    context = {'form': form}
    return render(request, 'new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            if topic.owner == request.user:
                new_entry.save()
        return HttpResponseRedirect(reverse('topic', args=[topic_id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topic', args=[topic.id]))
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'edit_entry.html', context)
