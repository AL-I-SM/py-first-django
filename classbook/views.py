from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Pupils, Days, Score
from .forms import SelectJournalForms
from django.core import serializers

# Create your views here.
def index(request):
    return render(request, 'classbook/index.html')


def journal_select(request):
    return redirect('journal', teacher=1, discipline=1, current_class=1)


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
        sc = {}
        pupils = Pupils.objects.filter(current_class_id=current_class)
        for pupil in pupils:
            sc.update([(pupil.id, {})])
            sc[pupil.id].update([(s.date, s.score) for s in scores.filter(pupil_id=pupil.id)])
        # todo придется тут раписать все по строкам, а там только готовые данные
        days = Days.objects.all()
        table = {'days': days, 'pupils': pupils,
                 # "form": scores_form,
                 'journal': journal, 'scores': sc}
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
            new_score = Score()
            new_score.date = Days.objects.get(pk=data.split()[0]).date
            new_score.pupil = Pupils.objects.get(pk=data.split()[1])
            new_score.score = score
            # new_score.teacher = None
            # new_score.discipline = None
            new_score.save()
    return HttpResponse(request.GET.keys())


