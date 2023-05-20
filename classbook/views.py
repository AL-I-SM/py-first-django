from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Pupils, Days, Score, Disciplines, Teachers
from .forms import SelectJournalForms
from django.core import serializers


def index(request):
    return render(request, 'classbook/index.html')


def journal_select(request):
    return redirect('journal', current_class=1, discipline=1, teacher=1)


@login_required
def journal(request, **kwargs):
    if request.method == "GET":
        current_class = kwargs['current_class']
        discipline = kwargs['discipline']
        teacher = kwargs['teacher']
        journal = SelectJournalForms()
        # scores_form = ScoresForms()
        scores = Score.objects.filter(pupil__current_class=current_class,
                                      discipline_id=discipline,
                                      teacher_id=teacher)
        pupils = Pupils.objects.filter(current_class_id=current_class)
        days = Days.objects.all()
        table = {'days': days, 'pupils': pupils,
                 # "form": scores_form,
                 'teacher': teacher, 'discipline': discipline,
                 'journal': journal, 'scores': scores}
        return render(request, 'classbook/journal.html', table)
    else:
        return redirect('journal',
                        teacher=request.POST['teacher'],
                        discipline=request.POST['discipline'],
                        current_class=request.POST['current_class'])
        # return HttpResponse(request.POST.items())


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
    return redirect('journal', current_class=2, discipline=1, teacher=9)
    # return HttpResponse(request.GET.keys())


