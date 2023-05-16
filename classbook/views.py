from django.shortcuts import render
from .models import Pupils, Days


# Create your views here.
def index(request):
    return render(request, 'classbook/index.html')


def journal(request):
    pupils = Pupils.objects.all()
    days = Days.objects.all()
    table = {'days': days, 'pupils': pupils}
    return render(request, 'classbook/journal.html', table)

