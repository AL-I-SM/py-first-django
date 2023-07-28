import datetime
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from pytils.translit import slugify
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from .models import Pupils, Days, Score, Disciplines, Schedule, Teachers, TimeLessons, Lessons, KTP, SCORE_CHOICES, \
    SIMPLE_SCORE_CHOICES, Classes
from .forms import SelectJournalForms, SelectTeacherScheduleForms, SelectGroupScheduleForms, PupilsForm, GroupsForm, \
    PupilEditForm
from django.core import serializers

LESSONS_TIME = [(8, 00), (9, 00), (10, 00), (11, 00), (12, 00), (13, 00)]

menu = {"Журнал": reverse_lazy('journal', args=[1, 1, 1]),
        "Расписание": reverse_lazy('schedule_class', args=[1]),
        "Ученики": reverse_lazy('pupils'),
        "Классы": reverse_lazy('groups'),
        }

types_of_lessons = {1: "Урок",
                    2: "Контрольная",
                    }


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
                                      discipline_id=self.discipline,
                                      deleted=False)
        pupils = Pupils.objects.filter(group_id=self.group)
        lessons = Lessons.objects.filter(group_id=self.group,
                                         discipline_id=self.discipline).order_by("date")
        ktp = self.get_next_lesson()
        table = {'lessons': lessons, 'pupils': pupils, 'ktp': ktp,
                 'teacher': self.teacher, 'discipline': self.discipline,
                 'select_journal': select_journal, 'scores': scores,
                 'types_of_lessons': types_of_lessons, 'all_menu': menu}
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
            if score in SIMPLE_SCORE_CHOICES and data.startswith('score'):
                if len(data.split()) == 4:
                    new_score = Score()
                if len(data.split()) > 4:
                    if score == '0':
                        for s in Score.objects.filter(
                                lesson_id=data.split()[1],
                                pupil_id=data.split()[2],
                                date=Lessons.objects.get(pk=data.split()[1]).date):
                            s.deleted = 1
                            s.save()
                        continue
                    else:
                        curr_score = ", ".join([s.score for s in Score.objects.filter(
                            lesson_id=data.split()[1],
                            pupil_id=data.split()[2],
                            date=Lessons.objects.get(pk=data.split()[1]).date,
                            deleted=False)])
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
                new_score.save()
        return redirect('journal', group=self.group, discipline=self.discipline, teacher=self.teacher)
        # return HttpResponse(request.GET.keys())


class ScheduleClassView(View):

    def get(self, request, *args, **kwargs):
        group = kwargs['group']
        group_name = Classes.objects.get(id=group).name
        select_schedule = SelectGroupScheduleForms(initial={'group': group})
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
                 'lessons_time': lessons_time, 'lessons': schedule,
                 'group': group_name, 'all_menu': menu}
        return render(request, 'classbook/schedule_class.html', table)

    def post(self, request, *args, **kwargs):
        return redirect('schedule_class',
                        group=request.POST['group'])


class ScheduleTeacherView(View):

    def get(self, request, *args, **kwargs):
        teacher = kwargs['teacher']
        schedule_select = SelectTeacherScheduleForms(initial={'teacher': teacher})
        schedule = Schedule.objects.filter(teacher_id=teacher)
        dt = datetime.datetime.today()
        md = datetime.date(dt.year, dt.month, dt.day) - datetime.timedelta(days=datetime.datetime.today().weekday())
        td = datetime.timedelta(days=1)
        lessons_time = TimeLessons.objects.filter(variant=1)
        days = (('ПН', md), ('ВТ', md + td), ('СР', md + td * 2),
                ('ЧТ', md + td * 3), ('ПТ', md + td * 4), ('СБ', md + td * 5))
        table = {'days': days, 'schedule_select': schedule_select,
                 'lessons_time': lessons_time, 'lessons': schedule,
                 'all_menu': menu}
        return render(request, 'classbook/schedule_teacher.html', table)

    def post(self, request, *args, **kwargs):
        return redirect('schedule_teacher',
                        teacher=request.POST['teacher'])


def index(request):
    return redirect('journal', group=1, discipline=1, teacher=1)
    # return render(request, 'classbook/index.html')


def journal_select(request):
    return redirect('journal', group=1, discipline=1, teacher=1)


def pupils(request):
    if request.method == 'POST':
        return redirect('pupils')
    pupils = Pupils.objects.all()
    # group = Classes.objects.get(name=form.cleaned_data['group'])
    context = {'pupils': pupils, 'all_menu': menu}
    return render(request, 'classbook/pupils.html', context)


class PupilUpdate(UpdateView):
    model = Pupils
    fields = "__all__"
    success_url = reverse_lazy("pupil")


def pupil_edit(request, *args, **kwargs):
    pupil = Pupils.objects.get(pk=kwargs['pupil'])
    form = PupilEditForm(request.POST or None, instance=pupil)
    if request.method == 'POST':
        if form.is_valid():
            pupil.save()
            return redirect('group_edit', group=pupil.group)
    # group = Classes.objects.get(name=form.cleaned_data['group'])
    context = {'form': form, 'pupils': pupils, 'all_menu': menu}
    return render(request, 'classbook/pupil_edit.html', context)


def groups(request):
    form = GroupsForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            group_name = form.cleaned_data['name']
            new_group = Classes(name=group_name)
            new_group.save()
            teacher = Teachers.objects.get(id=form.cleaned_data['teacher'])
            group_to_set = Classes.objects.get(name=form.cleaned_data['name'])
            teacher.has_class.add(group_to_set)
            return redirect('groups')
        else:
            pass
    groups = Classes.objects.all()
    context = {'form': form, 'groups': groups, 'all_menu': menu}
    return render(request, 'classbook/groups.html', context)


def group_edit(request, *args, **kwargs):
    form = PupilsForm(request.POST or None)
    if request.method == 'POST':
        # form.is_valid() make the form to submit only
        # when it contains CSRF Token
        if form.is_valid():
            # form.cleaned_data returns a dictionary of validated form input fields
            new_pupil = Pupils(first_name=form.cleaned_data['first_name'],
                               last_name=form.cleaned_data['last_name'],
                               middle_name=form.cleaned_data['middle_name'],
                               date_of_birth=form.cleaned_data['date_of_birth'],
                               group_id=kwargs['group'],
                               sex=form.cleaned_data['sex'],
                               # email="a@a.com",
                               username=slugify(form.cleaned_data['first_name'] + '-' + form.cleaned_data['last_name']),
                               # password="111",
                               # is_superuser=False,
                               # is_staff=False,
                               # is_active=True,
                               # date_joined="2010-01-01",
                               # last_login="2010-01-01",
                               sub_group=1
                               )
            new_pupil.save()
            return redirect('group_edit', group=kwargs['group'])
        else:
            pass
    pupils = Pupils.objects.filter(group_id=kwargs['group'])
    # group = Classes.objects.get(name=form.cleaned_data['group'])
    context = {'form': form, 'pupils': pupils, 'all_menu': menu}
    return render(request, 'classbook/group_edit.html', context)

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
