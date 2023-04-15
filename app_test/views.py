from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from .models import Topic
from .forms import TopicForm, EntryForm, Entry
from django.contrib.auth.decorators import login_required


menu = {"Админка": 'admin',
        "Плиткой": 'projects/',
        "Блог": 'blog/',
        "Участники": 'users/login/',
        "Темы": 'topics/'}


def index(request):
    return render(request, 'apts/index.html', {'all_menu': menu})


@login_required
def topics(request):
    # topics = Topic.objects.all().order_by('date_added')
    if request.user.is_superuser:
        topics = Topic.objects.all().order_by('date_added')
    else:
        topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'apts/topics.html', context)


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
    return render(request, 'apts/topic.html', context)


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
        return HttpResponseRedirect(reverse('apts:topics'))
    context = {'form': form}
    return render(request, 'apts/new_topic.html', context)


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
        return HttpResponseRedirect(reverse('apts:topic', args=[topic_id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'apts/new_entry.html', context)


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
            return HttpResponseRedirect(reverse('apts:topic', args=[topic.id]))
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'apts/edit_entry.html', context)
