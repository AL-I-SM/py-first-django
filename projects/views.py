from django.shortcuts import render
from projects.models import Project
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required


menu = {"Админка": 'admin/',
        "Журнал": 'classbook/',
        "Библиотека": 'catalog/',
        "Блог": 'blog/',
        "Участники": 'users/login/',
        }


def index(request):
    projects = Project.objects.all()
    context = {
        'projects': projects,
        'all_menu': menu
    }
    return render(request, 'projects/index.html', context)

def project_index(request):
    projects = Project.objects.all()
    context = {
        'projects': projects,
        'all_menu': menu
    }
    return render(request, 'project_index.html', context)


def project_detail(request, pk):
    project = Project.objects.get(pk=pk)
    context = {
        'project': project,
        'all_menu': menu
    }
    return render(request, 'project_detail.html', context)
