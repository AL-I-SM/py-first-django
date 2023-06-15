import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from .models import Pupils, Days, Score, Disciplines, Schedule, Teachers, TimeLessons, Lessons, KTP
from .forms import SelectJournalForms, SelectScheduleForms
from django.core import serializers

LESSONS_TIME = [(8, 00), (9, 00), (10, 00), (11, 00), (12, 00), (13, 00)]


# @method_decorator(login_required)
class JournalView(View):

    group = 1
    discipline = 1
    teacher = 1

    def get(self, request, *args, **kwargs):
        self.group = kwargs['group']
        self.discipline = kwargs['discipline']
        self.teacher = kwargs['teacher']
        select_journal = SelectJournalForms(initial={'teacher': self.teacher,
                                                     'discipline': self.discipline,
                                                     'group': self.group})
        scores = Score.objects.filter(pupil__group=self.group,
                                      discipline_id=self.discipline)
        pupils = Pupils.objects.filter(group_id=self.group)
        lessons = Lessons.objects.filter(group_id=self.group,
                                         discipline_id=self.discipline).order_by("date")
        ktp = self.get_next_lesson()
        table = {'lessons': lessons, 'pupils': pupils, 'ktp': ktp,
                 'teacher': self.teacher, 'discipline': self.discipline,
                 'select_journal': select_journal, 'scores': scores}
        return render(request, 'classbook/journal.html', table)

    def post(self, request, *args, **kwargs):
        # какие-нибудь параметры можно хранить и в сессии
        # request.session['teacher'] = request.POST['teacher']
        ## request.session.get("teacher")
        if request.POST.get('set_scores'):
            self.discipline = kwargs['discipline']
            self.teacher = kwargs['teacher']
            self.group = kwargs['group']
            self.score(request)
        if request.POST.get('add_lesson'):
            self.discipline = kwargs['discipline']
            self.teacher = kwargs['teacher']
            self.group = kwargs['group']
            self.add_lesson(request)
        if request.POST.get('get_journal'):
            self.discipline = request.POST['discipline']
            self.teacher = request.POST['teacher']
            self.group = request.POST['group']
        return redirect('journal',
                        teacher=self.teacher,
                        discipline=self.discipline,
                        group=self.group)

    def get_next_lesson(self):
        last_lesson = Lessons.objects.filter(group_id=self.group,
                                             discipline_id=self.discipline).order_by('-number').first()
        if not last_lesson:
            ktp = KTP.objects.filter(discipline_id=self.discipline).first()
        else:
            ktp = KTP.objects.filter(discipline_id=self.discipline,
                                     lesson_number=last_lesson.number + 1).first()
        return ktp

    def add_lesson(self, request):
        lesson = Lessons()
        lesson.group_id = self.group
        lesson.discipline_id = self.discipline
        lesson.teacher_id = self.teacher

        # ktp = self.get_next_lesson()
        lesson.number = request.POST['lesson_number']
        lesson.topic = request.POST['lesson_topic']
        lesson.home_work = request.POST['home_work']
        lesson.type = request.POST['lesson_type']
        lesson.date = datetime.datetime.now()
        lesson.save()

    def score(self, request):
        for data, score in request.POST.items():
            if score and data.startswith('score'):
                if len(data.split()) == 4:
                    new_score = Score()
                if len(data.split()) > 4:
                    curr_score = ", ".join([s.score for s in Score.objects.filter(
                                            lesson_id=data.split()[1],
                                            pupil_id=data.split()[2],
                                            date=Lessons.objects.get(pk=data.split()[1]).date)])
                    print(score, curr_score)
                    if score == curr_score:
                        continue
                    else:
                        new_score = Score()
                new_score.date = Lessons.objects.get(pk=data.split()[1]).date
                new_score.lesson_id = data.split()[1]
                new_score.score = score
                new_score.pupil_id = data.split()[2]
                new_score.teacher_id = data.split()[3]
                new_score.discipline = Lessons.objects.get(pk=data.split()[1]).discipline
                # new_score.pupil = Pupils.objects.get(pk=data.split()[1])
                # new_score.teacher = Teachers.objects.get(pk=data.split()[2])
                # new_score.discipline = Disciplines.objects.get(pk=data.split()[3])
                new_score.save()
        return redirect('journal', group=self.group, discipline=self.discipline, teacher=self.teacher)
        # return HttpResponse(request.GET.keys())


class ScheduleView(View):

    def get(self, request, *args, **kwargs):
        group = kwargs['group']
        select_schedule = SelectScheduleForms(initial={'group': group})
        schedule = Schedule.objects.filter(group_id=group)
        dt = datetime.datetime.today()
        md = datetime.date(dt.year, dt.month, dt.day) - datetime.timedelta(days=datetime.datetime.today().weekday())
        td = datetime.timedelta(days=1)
        # sd = md + td * 5
        lessons_time = TimeLessons.objects.filter(variant=1)
        days = (('ПН', md), ('ВТ', md + td), ('СР', md + td * 2),
                ('ЧТ', md + td * 3), ('ПТ', md + td * 4), ('СБ', md + td * 5))
        # days = Days.objects.all().filter(date__range=[md, sd]).order_by("date")
        table = {'days': days, 'schedule': select_schedule,
                 'lessons_time': lessons_time, 'lessons': schedule}
        return render(request, 'classbook/schedule.html', table)

    def post(self, request, *args, **kwargs):
        return redirect('schedule',
                        group=request.POST['group'])


def index(request):
    return render(request, 'classbook/index.html')


def journal_select(request):
    return redirect('journal', group=1, discipline=1, teacher=1)


# def score(request, *args, **kwargs):
#     for data, score in request.GET.items():
#         if score:
#             print(data.split())
#             if len(data.split()) == 4:
#                 new_score = Score()
#             if len(data.split()) > 4:
#                 new_score = Score.objects.get(id=data.split()[4])
#                 if score == str(new_score.score):
#                     continue
#             new_score.date = Lessons.objects.get(pk=data.split()[0]).date
#             new_score.lesson_id = data.split()[0]
#             new_score.score = score
#             new_score.pupil_id = data.split()[1]
#             new_score.teacher_id = data.split()[2]
#             new_score.discipline_id = data.split()[3]
#             # new_score.pupil = Pupils.objects.get(pk=data.split()[1])
#             # new_score.teacher = Teachers.objects.get(pk=data.split()[2])
#             # new_score.discipline = Disciplines.objects.get(pk=data.split()[3])
#             new_score.save()
#     return redirect('journal', group=2, discipline=2, teacher=9)
#     # return HttpResponse(request.GET.keys())