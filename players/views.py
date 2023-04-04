from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from .forms import UserForm
from .models import Person
from players.forms import CustomUserCreationForm


def index(request):
    people = Person.objects.all()
    return render(request, "players/index.html", {"people": people})


def edit(request, id):
    try:
        person = Person.objects.get(id=id)
        if request.method == "POST":
            person.name = request.POST.get("name")
            person.age = request.POST.get("age")
            person.save()
            return HttpResponseRedirect("/players")
        else:
            return render(request, "players/edit.html", {"person": person})
    except Person.DoesNotExist:
        return HttpResponseNotFound("<h2>Клиент не найден</h2>")


def delete(request, id):
    try:
        person = Person.objects.get(id=id)
        person.delete()
        return HttpResponseRedirect("/players")
    except Person.DoesNotExist:
        return HttpResponseNotFound("<h2>Клиент не найден</h2>")


def create(request):
    if request.method == "POST":
        klient = Person()
        klient.name = request.POST.get("name")
        klient.age = request.POST.get("age")
        klient.save()
    return HttpResponseRedirect("/players")


def dashboard(request):
    if request.method == "GET":
        userform = UserForm()
        # print(dir(userform))
        return render(request, 'players/dashboard.html', {"form": userform})
    else:
        name = request.POST.get("name")
        age = request.POST.get("age")
        return HttpResponse(name+age)


def register2(request):
    if request.method == "GET":
        return render(request, "players/register.html", {'form': CustomUserCreationForm})
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("players:dashboard"))
        else:
            return render(request, "players/register.html")
