from django.template.defaultfilters import register
import datetime

from classbook.models import Teachers

days = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб']


@register.filter()
def wd(day):
    return days[int(day) - 1]


@register.filter()
def add_weekday(obj, key):
    return str(key) + ", " + days[datetime.date.fromisoformat(str(key)).weekday()]


@register.filter()
def by_lesson(score_list_obj, key):
    """ """
    return [score for score in score_list_obj if score.lesson_id == key]


@register.filter()
def by_pupil(score_list_obj, key):
    """ """
    return [score for score in score_list_obj if score.pupil_id == key]


@register.filter()
def by_date(score_list_obj, key):
    """ """
    return [score for score in score_list_obj if score.date == key]


@register.filter()
def str_score(score_list_obj):
    """ """
    if not score_list_obj:
        return ""
    if len(score_list_obj) == 1:
        return score_list_obj[0].score
    if len(score_list_obj) > 1:
        return ", ".join([str(score.score) for score in score_list_obj])


@register.filter()
def id_score(score_list_obj):
    """ """
    if not score_list_obj:
        return ""
    if len(score_list_obj) == 1:
        return score_list_obj[0].score
    if len(score_list_obj) > 1:
        return ", ".join([str(score.id) for score in score_list_obj])


@register.filter()
def get_curator(query_obj, key):
    """ """
    try:
        curator = Teachers.objects.get(has_class__name=key.name)
    except:
        curator = 'нет куратора'
    return curator


@register.filter()
def by_numb_lesson(scedule_obj, numb):
    """ """
    return [scedule for scedule in scedule_obj if scedule.number_id == numb]


@register.filter()
def by_day_lesson(scedule_obj, day):
    """ """
    return [scedule for scedule in scedule_obj if scedule.day == days.index(day)]


@register.filter()
def get_discipline(scedule_obj):
    """ """
    return (scedule_obj.pop().discipline) if scedule_obj else ''


@register.filter()
def get_cabinet(scedule_obj):
    """ """
    return (scedule_obj.pop().cabinet) if scedule_obj else ''


@register.filter()
def get_discipline_and_cabinet(scedule_obj):
    """ """
    if scedule_obj:
        scedule_obj = scedule_obj.pop()
        return str(scedule_obj.cabinet) + ' ' + str(scedule_obj.discipline)
    return (scedule_obj.pop().cabinet) if scedule_obj else ''


@register.filter()
def by_teacher(scedule_obj, teacher):
    """ """
    return (scedule_obj.pop().teacher) if scedule_obj else ''


@register.filter()
def by_group(scedule_obj, key):
    """ """
    return [scedule for scedule in scedule_obj if scedule.group == key]
