from django.template.defaultfilters import register
import datetime

from classbook.models import Teachers

days = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ']


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
def by_numb_lesson(query_obj, key):
    """ """
    return query_obj.filter(number=key)


@register.filter()
def get_curator(query_obj, key):
    """ """
    try:
        curator = Teachers.objects.get(has_class__name=key.name)
    except:
        curator = 'нет куратора'
    return curator

@register.filter()
def by_day(query_obj, key):
    """ """
    data_lesson = query_obj.filter(day=datetime.date.fromisoformat(str(key)).weekday()).first()
    if data_lesson:
        return str(data_lesson.discipline) + ', ' + str(data_lesson.cabinet)
    else:
        return 'нет уроков'
        # return '<text color="gray">нет уроков</text>'

