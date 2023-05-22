from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from .models import Pupils, Days, Score, Disciplines, Schedule, Teachers
from .forms import SelectJournalForms
from django.core import serializers

LESSONS_TIME = [(8, 00), (9, 00), (10, 00), (11, 00), (12, 00), (13, 00)]


# @method_decorator(login_required)
class JournalView(View):

    def get(self, request, *args, **kwargs):
        group = kwargs['group']
        discipline = kwargs['discipline']
        teacher = kwargs['teacher']
        journal = SelectJournalForms(initial={'teacher': request.session.get("teacher"),
                                              'discipline': discipline,
                                              'group': group})
        # scores_form = ScoresForms()
        scores = Score.objects.filter(pupil__discipline=group,
                                      discipline_id=discipline,
                                      teacher_id=teacher)
        pupils = Pupils.objects.filter(group_id=group)
        days = Days.objects.all().order_by("date")
        table = {'days': days, 'pupils': pupils,
                 # "form": scores_form,
                 'teacher': teacher, 'discipline': discipline,
                 'journal': journal, 'scores': scores}
        return render(request, 'classbook/journal.html', table)

    def post(self, request, *args, **kwargs):
        # какие-нибудь параметры можно хранить и в сессии
        request.session['teacher'] = request.POST['teacher']
        return redirect('journal',
                        teacher=request.POST['teacher'],
                        discipline=request.POST['discipline'],
                        group=request.POST['group'])


class ScheduleView(View):

    def get(self, request, *args, **kwargs):
        group = 1  # kwargs['group']
        # schedule = ScheduleForms(initial={'group': group})
        schedule = Schedule.objects.filter(group__lessons=group)
        days = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ']
        mon_date = datetime.today() - timedelta(days=datetime.today().weekday())
        sut_date = mon_date + timedelta(days=6)
        days = Days.objects.all().filter(date__range=[mon_date, sut_date]).order_by("date")[:5]
        table = {'days': days, 'lessons': schedule,
                 'lessons_time': LESSONS_TIME}
        return render(request, 'classbook/schedule.html', table)

    def post(self, request, *args, **kwargs):
        return redirect('schedule',
                        group=request.POST['group'])


def index(request):
    return render(request, 'classbook/index.html')


def journal_select(request):
    return redirect('journal', group=1, discipline=1, teacher=1)


def score(request):
    for data, score in request.GET.items():
        if score:
            print(len(data.split()))
            if len(data.split()) == 4:
                new_score = Score()
            if len(data.split()) > 4:
                new_score = Score.objects.get(id=data.split()[4])
                if score == str(new_score.score):
                    continue
            new_score.date = Days.objects.get(pk=data.split()[0]).date
            new_score.pupil = Pupils.objects.get(pk=data.split()[1])
            new_score.score = score
            new_score.teacher = Teachers.objects.get(pk=data.split()[2])
            new_score.discipline = Disciplines.objects.get(pk=data.split()[3])
            new_score.save()
    return redirect('journal', group=2, discipline=1, teacher=9)
    # return HttpResponse(request.GET.keys())


